from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from users.models import Vendor, Buyer
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

class BuyerProduct(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_required = models.PositiveIntegerField()
    date_created = models.DateTimeField(default=timezone.now)
    image = models.ImageField(default='default.jpg', upload_to='product_pics')
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
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
        return f'{self.category.name}'

    class Meta:
        unique_together = (('category', 'product'),)

class BuyerProductCategory(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product = models.ForeignKey(BuyerProduct, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.category.name}'

    class Meta:
        unique_together = (('category', 'product'),)


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

    def __str__(self):
        return f'{self.author.username}'