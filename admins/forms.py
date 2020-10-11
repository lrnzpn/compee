from django import forms
from django.contrib.auth.models import User
from .models import (
    Product, Category, ProductCategory, 
    Service, ServiceCategory,
    ServiceItem, ServiceItemCategory
)

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

class ServiceCreateForm(forms.ModelForm):
    class Meta:
        model = Service
        fields =  ['name', 'description', 'price', 'discount_price', 'image', 'tags']
    
class AssignServiceCategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AssignServiceCategoryForm, self).__init__(*args, **kwargs)
        self.fields['category'].label = "Category"
    class Meta:
        model = ServiceCategory
        fields = ['category']

class ServiceItemCreateForm(forms.ModelForm):
    class Meta:
        model = ServiceItem
        fields = ['name', 'description', 'price', 'stock_required', 'image', 'tags']

class AssignItemCategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AssignItemCategoryForm, self).__init__(*args, **kwargs)
        self.fields['category'].label = "Category"
    class Meta:
        model = ServiceItemCategory
        fields = ['category']

