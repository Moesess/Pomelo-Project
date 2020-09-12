from django import template
from decimal import Decimal

register = template.Library()


@register.simple_tag()
def get_product(discount_id, discout_price, product_id, product_price):
    if discount_id == product_id:
        return discout_price
    else:
        return product_price


@register.simple_tag()
def get_product_price(product_price, quantity):
    return Decimal(product_price*quantity)
