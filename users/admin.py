from django.contrib import admin
from .models import Vendor, Buyer, VendorReview

admin.site.register(Vendor)
admin.site.register(Buyer)
admin.site.register(VendorReview)