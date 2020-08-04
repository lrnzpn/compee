from django import forms
from django.contrib.auth.models import User
from .models import Product, Category, ProductCategory, BuyerProduct, BuyerProductCategory

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

class BuyerProductCreateForm(forms.ModelForm):
    class Meta:
        model = BuyerProduct
        fields = ['name', 'description', 'price', 'stock_required', 'image', 'tags']

class AssignBuyerCategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AssignBuyerCategoryForm, self).__init__(*args, **kwargs)
        self.fields['category'].label = "Category"
    class Meta:
        model = BuyerProductCategory
        fields = ['category']