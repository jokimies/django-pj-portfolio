#
import factory

# Own
from portfolio.models import Security
from .price_tracker_factories import PriceTrackerFactory


class SecurityFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating securities
    """

    class Meta:
        model = Security

    # Security name by default will be 'Security 1' for the first created,
    # 'Category 2' for the second etc.
    name = factory.Sequence(lambda n: 'Security {0}'.format(n))

    # Same for ticker
    ticker = factory.Sequence(lambda n: 'Ticker {0}'.format(n))

    #
    price_tracker = factory.SubFactory(PriceTrackerFactory)
