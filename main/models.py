from django.db import models
from django.contrib.auth.models import User
from admins.models import Product
from django.utils import timezone

class WishlistItem(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.product.name}'

    class Meta:
        unique_together = (('user', 'product'),)

class CartItem(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_added = models.DateTimeField(default=timezone.now)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.product.name}'

    class Meta:
        unique_together = (('user', 'product'),)

STATUS_CHOICES = (
    ('Received','Received'),
    ('Shipped','Shipped'),
    ('Pending','Pending')
)
PAYMENT_CHOICES = (
    ('Cash on Delivery','Cash on Delivery'),
    ('PayMaya', 'PayMaya'),
    ('GCash','GCash')
)
class SiteOrder(models.Model):
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_placed = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default = ('Pending'))
    total = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=16, choices=PAYMENT_CHOICES, default=('Cash on Delivery'))
    address_line = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{self.user.username}'

class OrderItem(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(SiteOrder, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.product.name}'

    class Meta:
        unique_together = (('order', 'product'),)