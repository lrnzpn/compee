from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import SiteUser

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

class SiteUserUpdateForm(forms.ModelForm):
    class Meta:
        model = SiteUser
        fields = ['store_name', 'store_info', 'address_line', 'city','state','zip_code','date_joined', 'contact_no', 'secondary_no','image']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email']
