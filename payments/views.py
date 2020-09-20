from django.shortcuts import render
from main.models import SiteOrder, Transaction

def Payment(request, pk):
    transaction = Transaction.objects.get(transaction_id = pk)
    order = transaction.order
    total = order.total

    # PAYMENTS API METHOD HERE: Create Payments Token    
    import re
    if request.method == "POST":
        card_num = request.POST.get('card_num','')
        exp_date = request.POST.get('exp_date','')
        cvv = request.POST.get('cvv','')
        cardholder = request.POST.get('cardholder','')
        
        card_num = card_num.replace(" ", "")
        visa = re.match("^4[0-9]{12}(?:[0-9]{3})?$", card_num)
        mastercard = re.match("^5[1-5][0-9]{14}$", card_num)
        
        check_card = 0; check_exp = 0; status = 0
        
        if visa: check_card = 1
        elif mastercard: check_card = 1
        else: check_card = 0 # if card is invalid

        if int(exp_date[:2]) > 12: check_exp = 0
        else:
            if int(exp_date[-2:]) > 20: check_exp = 1 # check if year is greater than 20
            else: check_exp = 0
        
        if check_card == 1 and check_exp == 1: 
            status = 1
        elif (check_card == 1 and check_exp == 0) or (check_card == 0 and check_exp == 1):
            status = 0
        else: status = 0
        
        # do paymongo stuff
        from .paymongo import Paymongo
        paymongo = Paymongo()
        pi = ""; pm = ""

        # create payment intent
        intent = paymongo.PaymentIntent(int(total))
        pi = intent['data']['id']
        authurl = ''
        redirect_url = ''
        transaction_status = 0

        try:
            errors = intent['errors']
            # handle errors
            print(errors)
        except:
            # create payment method
            method = paymongo.PaymentMethod(int(card_num), int(exp_date[:2]), int('20' + exp_date[-2:]), int(cvv))
            try :
                errors = method['errors']
                print(errors)
            except:
                pm = method['data']['id']
                errors = []

                # Save intent and method to transaction
                transaction.pi = pi
                transaction.pm = pm
                transaction.save()

                redirect_url = 'http://'+ request.get_host() + reverse('my-orders')

                # Process payment
                attach = paymongo.AttachPaymentMethod(transaction.pi, transaction.pm, redirect_url)
                try:
                    # Handle errors
                    errors = attach['errors']

                    # Show Errors
                    print(errors)
                    
                    # Decline Transaction
                    transaction.status = 'Incomplete'
                    transaction.save()
                    # Include error details
                    transaction.order.status = "Pending"
                    transaction.order.cancel_reason = "Payment declined"
                    transaction.order.save()
                    
                    authurl = redirect_url
                    transaction_status = 3

                except:
                    # Complete transaction
                    transaction_status = attach['data']['attributes']['status']
                    if transaction_status == "succeeded":
                        transaction.status = 'Paid'
                        transaction.save()
                        authurl = redirect_url
                        transaction_status = 1
                    elif transaction_status == "awaiting_next_action" and attach['data']['attributes']['next_action']['type'] == 'redirect':
                        authurl = attach['data']['attributes']['next_action']['redirect']['url']
                        transaction_status = 2
                    else:
                        # Decline Transaction
                        transaction.status = 'Incomplete'
                        transaction.save()
                        # Include error details
                        transaction.order.status = "Pending"
                        trasaction.order.save()
                        authurl = redirect_url
                        transaction_status = 3

        data = {'card_num':card_num, 'exp_date': exp_date, 'cvv':cvv,'cardholder':cardholder, 'authurl': authurl, 'transaction_status': transaction_status, 'status': status, 'validate': {'check_card':check_card, 'check_exp': check_exp}}
        data = {'data': data, 'pi': pi, 'pm': pm, 'errors': errors}
        print(data)
        return HttpResponse(json.dumps(data), content_type="application/json")
    
    if 'confirm_card' in request.GET:
        # Update order as requested ONLY IF SUCCESSFUL
        if transaction.pi != '' or transaction.pm != '':
            transaction.order.status = 'Unfulfilled'
            transaction.order.save()
            # sms.send_sms(transaction.order, 'Requested')
            # send_mail.send_receipt_to_customer(request, transaction.order)
            # send_mail.send_email_to_merchant(request, transaction.order)
            data = {'valid': 1}
        else: data = {'valid': 0}
        return HttpResponse(json.dumps(data), content_type="application/json")

    context = {
        'title': 'Payment',
        'order': order,
        'transaction': transaction,
    }
    return render(request, 'payments/payment.html', context)