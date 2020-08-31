from django.contrib import admin
from .models import WishlistItem, CartItem, SiteOrder, OrderItem, PaymentMethod

admin.site.register(WishlistItem)
admin.site.register(CartItem)
admin.site.register(PaymentMethod)
admin.site.register(SiteOrder)
admin.site.register(OrderItem)
