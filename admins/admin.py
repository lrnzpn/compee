from django.contrib import admin
from .models import Product, Term, ProductTerm

admin.site.register(Product)
admin.site.register(Term)
admin.site.register(ProductTerm)