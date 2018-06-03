from django.core.management.base import BaseCommand
# Own imports
from ...models import PriceTracker


class Command(BaseCommand):

    def handle(self, **options):

        trackers = ['Kauppalehti',  'GoogleFinance', 'AlphaVantage' ]

        for tracker in trackers:
            if not PriceTracker.objects.filter(name=tracker):
                PriceTracker.objects.create(name=tracker)
                print("Creating {}".format(tracker))
