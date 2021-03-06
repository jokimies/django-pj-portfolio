# 3rd party
from django.utils import timezone
import factory
# Own
from portfolio.models import Price

from .security_factories import SecurityFactory
from .currency_factories import CurrencyFactory


#############
#
# Factories
#
#############

class PriceFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating securities
    """

    class Meta:
        model = Price

    price = 19.30
    date = timezone.now()
    security = factory.SubFactory(SecurityFactory)
    currency = factory.SubFactory(CurrencyFactory)
    change = 0.03
    change_percentage = 0.12

