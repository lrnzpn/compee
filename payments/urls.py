from django.urls import path
import payments.views as v

urlpatterns = [
    path('checkout/paypal-payment/<str:pk>/', v.PaypalPayment, name="credit-payment"),
    path('checkout/payment/<str:pk>/', v.OtherPayment, name='other-payment'),
    path('success/', v.PaymentSuccess, name='payment-success'),
    path('checkout/payment-method/<str:pk>/', v.ChoosePaymentMethod, name="payment-method")
]