from admins.models import Service, ServiceReview
from django import template

register = template.Library()

@register.filter(name='find_serv_review_id')
def find_prod_review_id(pk, user):
    service = Service.objects.get(service_id=pk)
    return ServiceReview.objects.get(author=user, service=service).review_id