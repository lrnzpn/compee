from django.db import models
from django.contrib.auth.models import User
from admins.models import Product, ShippingRate
from django.utils import timezone
import datetime
import uuid
from django.core.validators import RegexValidator

numericCheck = RegexValidator(r'^\d+$', 'Only numeric characters are allowed.')

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
    ('Payment Pending','Payment Pending'),
    ('Unfulfilled', 'Unfulfilled'),
    ('Cancelled', 'Cancelled')
)

class PaymentMethod(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    details = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.title}'


class SiteOrder(models.Model):
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contact_no = models.CharField(max_length=15, validators=[numericCheck])
    date_placed = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default = ('Unfulfilled'))
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_method = models.ForeignKey(PaymentMethod, blank=True, null=True, on_delete=models.SET_NULL)
    address_line = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.PositiveSmallIntegerField()
    shipping_fee = models.ForeignKey(ShippingRate, blank=True, null=True, on_delete=models.SET_NULL)

    def get_ref_id():
        ref_id = datetime.datetime.now().strftime('%y%m%d%H%M%S') + str(uuid.uuid4().hex[:6].upper())
        print("CALL COUNT: " + ref_id)
        return ref_id

    ref_id = models.CharField(max_length=100, blank=True, unique=True, default=get_ref_id())

    def __str__(self):
        return f'{self.user.username}'

class OrderItem(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(SiteOrder, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.product.name}'

    class Meta:
        unique_together = (('order', 'product'),)