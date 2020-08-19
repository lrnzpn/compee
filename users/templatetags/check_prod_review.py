from admins.models import Product, ProductReview
from django import template

register = template.Library()

@register.filter(name='check_prod_review')
def check_prod_review(pk, user):
    product = Product.objects.get(product_id=pk)
    return ProductReview.objects.filter(author=user, product=product).exists()