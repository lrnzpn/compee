from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from users.models import Vendor, ServiceProvider
from PIL import Image
from taggit.managers import TaggableManager 

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    item_stock = models.PositiveIntegerField()
    date_created = models.DateTimeField(default=timezone.now)
    image = models.ImageField(default='default.jpg', upload_to='product_pics')
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, max_length=100)
    tags = TaggableManager()

    def __str__(self):
        return f'{self.name}' 

    def save(self):
        super().save()
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)

class ServiceItem(models.Model):
    item_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_required = models.PositiveIntegerField()
    date_created = models.DateTimeField(default=timezone.now)
    image = models.ImageField(default='default.jpg', upload_to='product_pics')
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, max_length=100)
    tags = TaggableManager()

    def __str__(self):
        return f'{self.name}' 

    def save(self):
        super().save()
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)

class Service(models.Model):
    service_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    date_created = models.DateTimeField(default=timezone.now)
    image = models.ImageField(default='default.jpg', upload_to='product_pics')
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, max_length=100)
    tags = TaggableManager()

    def __str__(self):
        return f'{self.name}' 

    def save(self):
        super().save()
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}' 

class ProductCategory(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.category.name} - {self.product.name}'

    class Meta:
        unique_together = (('category', 'product'),)

class ServiceCategory(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.category.name} - {self.service.name}'

    class Meta:
        unique_together = (('category', 'service'),)

class ServiceItemCategory(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    service_item = models.ForeignKey(ServiceItem, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.category.name} - {self.service_item.name}'

    class Meta:
        unique_together = (('category', 'service_item'),)


RATING_CHOICES = (
    ('1','1'),
    ('2','2'),
    ('3', '3'),
    ('4', '4'),
    ('5','5')
)

class ProductReview(models.Model):
    review_id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.CharField(max_length=1, choices=RATING_CHOICES, default=('3'))
    description = models.TextField(blank=True, null=True)
    order = models.ForeignKey('main.SiteOrder', on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{product.name} Review - {self.author.username}'

class ServiceReview(models.Model):
    review_id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    rating = models.CharField(max_length=1, choices=RATING_CHOICES, default=('3'))
    description = models.TextField(blank=True, null=True)
    order = models.ForeignKey('main.SiteOrder', on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{service.name } Review - {self.author.username}'

class ShippingRate(models.Model):
    id = models.AutoField(primary_key=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'

class VendorShipping(models.Model):
    id = models.AutoField(primary_key=True)
    rate = models.ForeignKey(ShippingRate, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.vendor.store_name} {self.rate.rate}'

    class Meta:
        unique_together = (('rate', 'vendor'),)

class CompeeCaresRate(models.Model):
    id = models.AutoField(primary_key=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.rate}'

class ProductGuide(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True, max_length=100)
