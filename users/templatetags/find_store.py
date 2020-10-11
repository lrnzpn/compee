from users.models import Vendor, ServiceProvider
from django.contrib.auth.models import User
from django import template

register = template.Library()

@register.filter(name='find_store')
def find_store(pk, type):
    user = User.objects.get(id=pk)
    if type == "Provider":
        return ServiceProvider.objects.get(user=user).provider_id
    elif type == "Vendor":
        return Vendor.objects.get(user=user).vendor_id