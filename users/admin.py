from django.contrib import admin
from .models import Vendor, ServiceProvider, VendorReview, ProviderReview

admin.site.register(Vendor)
admin.site.register(ServiceProvider)
admin.site.register(VendorReview)
admin.site.register(ProviderReview)