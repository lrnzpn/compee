from django.contrib import admin
from .models import (
    Product, ServiceItem, Service,
    Category, ProductCategory, ServiceCategory, ServiceItemCategory,
    ProductReview, ServiceReview, ShippingRate, VendorShipping, 
    CompeeCaresRate, ProductGuide
)

admin.site.register(Product)
admin.site.register(ServiceItem)
admin.site.register(Service)
admin.site.register(Category)
admin.site.register(ProductCategory)
admin.site.register(ServiceCategory)
admin.site.register(ServiceItemCategory)
admin.site.register(ProductReview)
admin.site.register(ServiceReview)
admin.site.register(ShippingRate)
admin.site.register(VendorShipping)
admin.site.register(CompeeCaresRate)
admin.site.register(ProductGuide)