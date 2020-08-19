from admins.models import Product, ProductReview
from django import template

register = template.Library()

@register.filter(name='find_prod_review_id')
def find_prod_review_id(pk, user):
    product = Product.objects.get(product_id=pk)
    return ProductReview.objects.get(author=user, product=product).review_id