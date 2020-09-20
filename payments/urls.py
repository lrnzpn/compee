from django.urls import path
import payments.views as v

urlpatterns = [
    path('checkout/payment/<str:pk>/', v.Payment, name="payment")
]