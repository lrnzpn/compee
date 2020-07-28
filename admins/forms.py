from django import forms
from django.contrib.auth.models import User
from .models import Product, Term, ProductTerm

class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'discount_price', 'item_stock', 'image']

class AssignCategoryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AssignCategoryForm, self).__init__(*args, **kwargs)
        self.fields['term'].label = "Category"
    class Meta:
        model = ProductTerm
        fields = ['term']

