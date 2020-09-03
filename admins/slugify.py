from django.template.defaultfilters import slugify
from django.utils.crypto import get_random_string

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