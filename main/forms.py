from django import forms
from .models import CompeeCaresRenewal, OrderItem

class RenewalForm(forms.ModelForm):

    def __init__(self, order, *args, **kwargs):
        super(RenewalForm, self ).__init__(*args,**kwargs)
        self.fields['order_item'].queryset = OrderItem.objects.filter(order=order)

    class Meta:
        model = CompeeCaresRenewal
        fields = ['order_item', 'notes']

class ContactForm(forms.Form):
    from_email = forms.EmailField(label="Your Email")
    subject = forms.CharField(label="Subject")
    message = forms.CharField(label="Message",widget=forms.Textarea)