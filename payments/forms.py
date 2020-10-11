from django import forms
from main.models import SiteOrder

class UpdatePaymentMethodForm(forms.ModelForm):
    class Meta:
        model = SiteOrder
        fields = ['payment_method']