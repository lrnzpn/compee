from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from PIL import Image
from django.utils.timezone import now


numericCheck = RegexValidator(r'^\d+$', 'Only numeric characters are allowed.')

STATUS_CHOICES = (
    ('Active', 'Active'),
    ('Inactive', 'Inactive'),
)

class Vendor(models.Model):
    vendor_id = models.AutoField(primary_key=True)
    store_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=100)
    store_info = models.TextField(blank=True, null=True)
    address_line = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    zip_code = models.PositiveSmallIntegerField(blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    contact_no = models.CharField(max_length=15, blank=True, null=True, validators=[numericCheck])
    secondary_no = models.CharField(max_length=15, blank=True, null=True, validators=[numericCheck])
    image = models.ImageField(default='default.jpg', upload_to='store_pics')
    about_image = models.ImageField(blank=True, null=True, upload_to='store_pics')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default = ('Inactive'))

    def __str__(self):
        return f'{self.store_name}' 

    def save(self):
        super().save()
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)
    
    def month_diff(self):
        return now().month - self.date_joined.month

class ServiceProvider(models.Model):
    provider_id = models.AutoField(primary_key=True)
    store_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True,max_length=100)
    provider_info = models.TextField(blank=True, null=True)
    address_line = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50,blank=True, null=True)
    zip_code = models.PositiveSmallIntegerField(blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    contact_no = models.CharField(max_length=15, blank=True, null=True, validators=[numericCheck])
    secondary_no = models.CharField(max_length=15, blank=True, null=True, validators=[numericCheck])
    image = models.ImageField(default='default.jpg', upload_to='store_pics')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.store_name}' 

RATING_CHOICES = (
    ('1','1'),
    ('2','2'),
    ('3', '3'),
    ('4', '4'),
    ('5','5')
)

class VendorReview(models.Model):
    review_id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    rating = models.CharField(max_length=1, choices=RATING_CHOICES, default=('3'))
    description = models.TextField(blank=True, null=True)
    order = models.ForeignKey('main.SiteOrder', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.vendor.store_name} Review - {self.author.username}'

class ProviderReview(models.Model):
    review_id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    rating = models.CharField(max_length=1, choices=RATING_CHOICES, default=('3'))
    description = models.TextField(blank=True, null=True)
    order = models.ForeignKey('main.SiteOrder', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.provider.store_name} Review - {self.author.username}'

