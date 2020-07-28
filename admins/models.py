from django.db import models
from django.utils import timezone
from users.models import Vendor
from PIL import Image

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    item_stock = models.PositiveIntegerField()
    date_created = models.DateTimeField(default=timezone.now)
    image = models.ImageField(default='default.jpg', upload_to='product_pics')
    vendor = models.ForeignKey(Vendor, models.DO_NOTHING)

    def __str__(self):
        return f'{self.name}' 

    def save(self):
        super().save()
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)

TYPE_CHOICES = (
    ('Category','Category'),
    ('Tag','Tag'),
)

class Term(models.Model):
    term_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    term_type = models.CharField(max_length=8, choices=TYPE_CHOICES, default=('Category'))

    def __str__(self):
        return f'{self.name}' 

class ProductTerm(models.Model):
    id = models.AutoField(primary_key=True)
    term = models.ForeignKey(Term, models.DO_NOTHING)
    product = models.ForeignKey(Product, models.CASCADE)

    class Meta:
        unique_together = (('term', 'product'),)