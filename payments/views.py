from django.shortcuts import render, reverse, redirect
from main.models import SiteOrder
import json
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseRedirect
from django.contrib import messages
from .forms import UpdatePaymentMethodForm
from users.forms import UserRegisterForm

def PaypalPayment(request, pk):
    if SiteOrder.objects.filter(ref_id=pk).exists():
        order = SiteOrder.objects.get(ref_id=pk)
        if order.user == request.user and order.status == "Payment Pending" and order.payment_method.title == "Paypal or Debit/Credit Card":
            return render(request, 'payments/credit_payment.html', {'order':order})
        else:
            return redirect('my-orders')
    else:
        messages.error(request, 'Order does not exist.')
        return redirect('my-orders')

def PaymentSuccess(request):
    body = json.loads(request.body)
    print('BODY:' + str(body))
    order = SiteOrder.objects.get(ref_id=body['orderId'])
    order.status = "Unfulfilled"
    order.save()
    return JsonResponse('Payment completed!', safe=False)

def OtherPayment(request, pk):
    if SiteOrder.objects.filter(ref_id=pk).exists():
        order = SiteOrder.objects.get(ref_id=pk)
        invalidmethods = ['Cash On Delivery', 'Paypal or Debit/Credit Card']
        if order.user == request.user and order.status == "Payment Pending" and order.payment_method.title not in invalidmethods:
            return render(request, 'payments/other_payment.html', {'order':order})
        else:
            return redirect('my-orders')
    else:
        messages.error(request, 'Order does not exist.')
        return redirect('my-orders')


def ChoosePaymentMethod(request, pk):
    if SiteOrder.objects.filter(ref_id=pk).exists():
        order = SiteOrder.objects.get(ref_id=pk)
        if order.user == request.user and order.status == "Payment Pending":
            if request.method == "POST":
                form = UpdatePaymentMethodForm(request.POST, instance=order)
                if form.is_valid():
                    new = form.save()
                    if new.payment_method.title == "Paypal or Debit/Credit Card":
                        return redirect('credit-payment', new.ref_id)
                    elif new.payment_method.title == "Cash On Delivery":
                        new.status = "Unfulfilled"
                        new.save()
                        messages.success(request, "Payment method updated")
                        return redirect('my-orders')
                    else:
                        return redirect('other-payment', new.ref_id)
            else:
                form = UpdatePaymentMethodForm(instance=order)
            context = {
                'form':form,
                'order':order
            }
            return render(request, 'payments/choose_payment.html',context)
        else:
            return redirect('my-orders')
    else:
        messages.error(request, 'Order does not exist')
        return redirect('my-orders')

