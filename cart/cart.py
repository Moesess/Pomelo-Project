from decimal import Decimal
from django.conf import settings
from pomelo.models import *


class Cart(object):

    def __init__(self, request):
        """
        Inicjalizacja koszyka na zakupy
        """

        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            # zapisuje pusty koszyk
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        """
        Dodanie produktu do koszyka lub zmiana ilosci
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            try:
                discount_percent = 100 - product.product_discount.discount
                if discount_percent < 1:
                    discount_percent = 1
                if discount_percent > 100:
                    discount_percent = 100
                price = (product.price * discount_percent/100).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)
            except:
                price = product.price

            self.cart[product_id] = {
                'quantity': 0,
                'price': str(price)
            }
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # uaktualnienie koszyka
        self.session[settings.CART_SESSION_ID] = self.cart
        # oznaczenie sesji jako zmodyfikowana
        self.session.modified = True

    def remove(self, product):
        """
        Usuwanie produktu z koszyka
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Iteraacja przez elementy koszyka i pobranie produktow z bazy
        """
        product_ids = self.cart.keys()
        # pobranie obiektow produktow i dodanie ich do koszyka
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Obliczenie ilosci produktow
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        # usuniecie koszyka
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
