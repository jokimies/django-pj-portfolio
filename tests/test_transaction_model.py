# 3rd party
from django.test import TestCase
from django.utils import timezone

import factory

# Own

from portfolio.models import Transaction

from .test_security_model import SecurityFactory
from .account_factories import AccountFactory
from .currency_factories import CurrencyFactory

class TransactionFactory(factory.django.DjangoModelFactory):
    """ 
    Factory for creating transacions
    """

    class Meta:
        model = Transaction

    account = factory.SubFactory(AccountFactory)
    action = 'BUY'
    date = timezone.now()
    security = factory.SubFactory(SecurityFactory)
    shares = 100
    price = 21.30
    commission = 0
    currency = factory.SubFactory(CurrencyFactory)

#########
# 
# Tests
#
#########

class TransactionModelTest(TestCase):
    
    longMessage = True

    def create_transaction(self, **kwargs):
        return TransactionFactory(**kwargs)

    def setUp(self):
        self.transaction = self.create_transaction()
        self.transaction.save()
        self.security = SecurityFactory(name='Elisa')
        self.currency = CurrencyFactory(iso_code='EUR')

    def test_saving_transaction(self):
        TransactionFactory(security=self.security)
        saved_items = Transaction.objects.all()
        # 2: one created above and the other in setUp()
        self.assertEqual(saved_items.count(), 2,
                         'Should be two securities in db')
        
    def test_edit_transaction(self):
        self.create_transaction(security=self.security) 
        transaction = Transaction.objects.latest('date')
        transaction.price = 22.54
        transaction.currency = self.currency
        transaction.save()

        edited_transaction = Transaction.objects.get(pk=transaction.pk)

        self.assertEquals(float(edited_transaction.price), 22.54)
        self.assertEquals(edited_transaction.currency.iso_code, 'EUR')
