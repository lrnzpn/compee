import requests
from django.conf import settings

public_key = settings.PAYMONGO_PK
private_key = settings.PAYMONGO_SK


class Paymongo:
    # 1. CREATE PAYMENT INTENT
    # You should create your payment intent from your backend using your secret API key then send the client_key of the response to the client-side. 
    # This client_key will be used to attach a payment method to the payment intent. 
    # In this step, the payment intent's status is awaiting_payment_method.
    
    def PaymentIntent(self, amount):

        url = "https://api.paymongo.com/v1/payment_intents"
        payload = "{\"data\":{\"attributes\":{\"amount\":" + str(amount) + ",\"payment_method_allowed\":[\"card\"],\"payment_method_options\":{\"card\":{\"request_three_d_secure\":\"any\"}},\"currency\":\"PHP\",\"description\":\"Ventii Eats\"}}}"
        headers = {
            'accept': "application/json",
            'content-type': "application/json",
            'authorization': "Basic " + private_key
            }

        response = requests.request("POST", url, data=payload, headers=headers)
        data = response.json()
        print(data)
        return data

    # 2. ATTACH PAYMENT METHOD
    # From the client-side, the collected credit card information must be sent to PayMongo by creating a PaymentMethod.
    # Attach it to the Payment Intent using the client_key as the Payment Intent identifier and your public API key for authentication. 
    # For better user experience, an asynchronous call is highly recommended to lessen page redirections.

    def PaymentMethod(self, cardnum, exp_month, exp_year, cvc):
        
        url = "https://api.paymongo.com/v1/payment_methods"
        payload = "{\"data\":{\"attributes\":{\"details\":{\"card_number\":\""+ str(cardnum) + "\",\"exp_month\":" + str(exp_month) + ",\"exp_year\":" + str(exp_year) + ",\"cvc\":\"" + str(cvc) + "\"},\"type\":\"card\"}}}"
        headers = {
            'accept': "application/json",
            'content-type': "application/json",
            'authorization': "Basic " + public_key
            }

        response = requests.request("POST", url, data=payload, headers=headers)
        data = response.json()
        print(data)
        return data

    def AttachPaymentMethod(self, pi, pm, redirect_url):
        url = "https://api.paymongo.com/v1/payment_intents/" + str(pi) + "/attach"
        payload = "{\"data\":{\"attributes\":{\"return_url\":\"" + str(redirect_url) +"\",\"payment_method\":\"" + str(pm) + "\"}}}"
        headers = {
            'accept': "application/json",
            'content-type': "application/json",
            'authorization': "Basic " + private_key
            }
        response = requests.request("POST", url, data=payload, headers=headers)
        data = response.json()
        print(data)
        return data

    def RetrievePayment(self, pi):
        url = "https://api.paymongo.com/v1/payment_intents/" + pi
        headers = {
            'authorization': "Basic " + private_key
            }

        response = requests.request("GET", url, headers=headers)
        data = response.json()
        print(data)
        return data
    
    def CreateSource(self, amount):
        secretkey = ''
        payload =  {
                    "data": {
                        "attributes": {"type": "gcash",
                                "amount": amount,
                                "currency": "PHP",
                                "redirect": {
                                    "success": "https://wela.online",
                                    "failed": "https://bai.ph"
                                }
                            }
                        }
                    }

        response = requests.post(payment_source_url, data=json.dumps(payload), headers=headers,
                                 auth=(secret_key, ''))
        json_response = response.json()
        return {"id": json_response['data']['id'],
                "checkout_url": json_response['data']['attributes']['redirect']['checkout_url']}
