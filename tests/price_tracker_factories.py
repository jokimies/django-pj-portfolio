#
import factory

# Own
from portfolio.models import PriceTracker


#############
#
# Factories
#
#############

class PriceTrackerFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating PriceTrackers
    """

    class Meta:
        model = PriceTracker

    # Tracker name by default will be 'Tracker 1' for the first created,
    # 'Tracker 2' for the second etc.
    name = factory.Sequence(lambda n: 'Tracker {0}'.format(n))
