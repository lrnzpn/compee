from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Vendor, ServiceProvider

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    username = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    password1 = forms.CharField(widget=forms.TextInput(attrs={'type':'password'}))
    password2 = forms.CharField(widget=forms.TextInput(attrs={'type':'password'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        labels  = {
            'email': 'Email',
            'username':'Username',
            'first_name':'First Name',
            'last_name':'Last Name', 
            'password1': 'Password',
            'password2':'Password confirm'
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email']

class PasswordResetForm(forms.ModelForm):
    oldpassword = forms.CharField(required= False,label="Current Password", max_length = 20, widget=forms.TextInput(attrs={'type':'password',  'class' : 'span'}))
    newpassword1 = forms.CharField(required= False,label="New Password", max_length = 20, widget=forms.TextInput(attrs={'type':'password', 'class' : 'span'}))
    newpassword2 = forms.CharField(required= False,label="Confirm New Password", max_length = 20, widget=forms.TextInput(attrs={'type':'password', 'class' : 'span'}))

    def clean(self):
        if 'newpassword1' in self.cleaned_data and 'newpassword2' in self.cleaned_data:
            if self.cleaned_data['newpassword1'] != self.cleaned_data['newpassword2']:
                raise forms.ValidationError(("The two password fields did not match."))
        return self.cleaned_data
    
    class Meta:
        model = User
        fields = []

class VendorUpdateForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['store_name', 'store_info', 'address_line', 'city', 'state', 
                'zip_code', 'contact_no', 'secondary_no', 'image']

class ProviderUpdateForm(forms.ModelForm):
    class Meta:
        model = ServiceProvider
        fields = ['store_name', 'provider_info', 'address_line', 'city', 'state', 
                'zip_code', 'contact_no', 'secondary_no', 'image']

class ProviderCreateForm(forms.ModelForm):
    class Meta:
        model = ServiceProvider
        fields = ['store_name', 'provider_info', 'address_line', 'city', 'state', 
                'zip_code', 'contact_no', 'secondary_no']

class ProviderDeleteForm(forms.ModelForm):
    class Meta:
        model = ServiceProvider
        fields = []

class AdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = []


