from django import template
from math import floor

register=template.Library()

@register.simple_tag
def call_sellprice(price,discount):
    if discount is None or discount == 0:
        return price
    sellprice=price
    sellprice=price - (price * discount/100)
    return floor(sellprice)