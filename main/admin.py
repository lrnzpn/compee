from django.contrib import admin
from .models import WishlistItem, CartItem, SiteOrder, OrderItem

admin.site.register(WishlistItem)
admin.site.register(CartItem)
admin.site.register(SiteOrder)
admin.site.register(OrderItem)
