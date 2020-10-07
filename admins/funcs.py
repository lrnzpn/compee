from django.template.defaultfilters import slugify
from django.utils.crypto import get_random_string
from users.models import Vendor
from admins.models import VendorShipping
import datetime
import uuid

def unique_product_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.name)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
                    slug=slug,
                    randstr=get_random_string(length=4)
                )
        return unique_product_slug_generator(instance, new_slug=new_slug)
    return slug

def unique_store_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.store_name)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
                    slug=slug,
                    randstr=get_random_string(length=4)
                )
        return unique_product_slug_generator(instance, new_slug=new_slug)
    return slug

def updateVendorStatus():
    vendors = Vendor.objects.all()
    notset = False
    for v in vendors:
        if v.status == "Active" and not VendorShipping.objects.filter(vendor=v).exists():
            notset = True
            v.status = "Inactive"
            v.save()
    return notset
        

def get_ref_id():
    ref_id = datetime.datetime.now().strftime('%y%m%d%H%M%S') + str(uuid.uuid4().hex[:6].upper())
    return ref_id