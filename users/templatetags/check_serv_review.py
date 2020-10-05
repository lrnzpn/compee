from admins.models import Service, ServiceReview
from django import template

register = template.Library()

@register.filter(name='check_serv_review')
def check_prod_review(pk, user):
    service = Service.objects.get(service_id=pk)
    return ServiceReview.objects.filter(author=user, service=service).exists()