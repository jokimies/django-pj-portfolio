## factory boy
import factory

# Own
from portfolio.models import Account

class AccountFactory(factory.django.DjangoModelFactory):

    """
    Factory for creating accounts
    """

    class Meta:
        model = Account

    # Account name by default will be 'Account 1' for the first created
    # account, 'Account 2' for the next and so on

    name = factory.Sequence(lambda n: 'Account {0}'.format(n))
    base_currency = 'EUR'
