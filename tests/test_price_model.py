
# 3rd party
from django.test import TestCase

# Own
from portfolio.models import Price
from .price_factories import PriceFactory

#########
#
# Tests
#
#########

class PriceModelTest(TestCase):

    longMessage = True

    def create_price(self, price=None, security=None):
        """
        Create price
        If price is given, also assumes that security is given
        Returns price
        """

        if not price:
            return PriceFactory()
        return PriceFactory(price=price, security=security)
        
    def test_saving_price(self):

        price1 = self.create_price()
        price2 = self.create_price()
        
        saved_items = Price.objects.all()
        self.assertEqual(saved_items.count(), 2,
                         'Should be two prices in db')

