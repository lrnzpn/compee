from django import forms
from django.contrib.auth.models import User
from .models import Product, Category, ProductCategory

class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'discount_price', 'item_stock', 'image', 'tags']

class AssignCategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AssignCategoryForm, self).__init__(*args, **kwargs)
        self.fields['category'].label = "Category"
    class Meta:
        model = ProductCategory
        fields = ['category']