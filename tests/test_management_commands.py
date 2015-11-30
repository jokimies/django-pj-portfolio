from django.core.management import call_command
from django.test import TestCase

from portfolio.models import PriceTracker, Price, Security

from .security_factories import SecurityFactory
from .currency_factories import CurrencyFactory
from .price_tracker_factories import PriceTrackerFactory


class UpdatePrices(TestCase):
    """
    Tests management commands
    """

    longmessage = True

    def setUp(self):

        # Testing runs migrations and one of them, while adding
        # price_tracker field to Security, calls set_default_tracker, which
        # in turn creates the named tracker if not already exists in the
        # DB.
        # Hence, there already is one tracker in DB when tests beging

        # For now, Kaupplaheti is the one created before testing
        # starts. Get that tracker (or create if it does not exist)
        self.tracker_kl, created = PriceTracker.objects.get_or_create(
            name='Kauppalehti')
        self.tracker_google = PriceTrackerFactory(name='GoogleFinance')
        self.security = SecurityFactory(name='Elisa', ticker='ELI1V', 
                                   price_tracker=self.tracker_kl)
        self.currency = CurrencyFactory(iso_code='EUR')

    def test_update_share_prices(self):

        call_command('update_share_prices')
    
    def test_update_trackers_dont_store_duplicates(self):
        """
        Test trackers are not entered into DB twice
        setUp() created same trackers update_price_trackers would
        """

        call_command('update_price_trackers')
        self.assertEqual(PriceTracker.objects.count(), 2)

    def test_update_trackers_stores_trackers(self):

        # First delete trackers created in setUp():
        self.tracker_kl.delete()
        self.tracker_google.delete()
        self.assertEqual(PriceTracker.objects.count(),0)

        # Then create those again
        call_command('update_price_trackers')
        self.assertEqual(PriceTracker.objects.count(), 2)
        
    def test_price_is_stored_only_once_per_day(self):
        
        call_command('update_share_prices')
        call_command('update_share_prices')
        self.assertEqual(Price.objects.filter(
            security=self.security).count(), 1)
