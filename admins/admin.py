from django.contrib import admin
from .models import (
    Product, ServiceItem, Service,
    Category, ProductCategory, ServiceCategory, ServiceItemCategory,
    ProductReview, ServiceReview, ShippingRate, VendorShipping, 
    CompeeCaresRate, ProductGuide, Faq, DisplayGroup, ProductGroup,
    Banner
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
admin.site.register(Faq)
admin.site.register(DisplayGroup)
admin.site.register(ProductGroup)
admin.site.register(Banner)