from django.urls import path
import payments.views as v

urlpatterns = [
    path('p', v.Payment, name="payment")
]