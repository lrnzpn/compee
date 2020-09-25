from django.contrib import admin
from .models import Product, Category, ProductCategory, ProductReview, BuyerProduct, BuyerProductCategory

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(ProductCategory)
admin.site.register(ProductReview)
admin.site.register(BuyerProduct)
admin.site.register(BuyerProductCategory)