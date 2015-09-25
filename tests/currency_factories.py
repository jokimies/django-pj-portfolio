#
# Factory for Currency
#

# 3rd party
import factory

from currency_history.models import Currency, CurrencyRate, CurrencyRateHistory

# Taken from currency_history/tests/factories.py
#
class CurrencyFactory(factory.django.DjangoModelFactory):

    """
    Factory for creating currencies
    """
    class Meta:
        model = Currency

    # Currency iso-code  by default will be 'ISO 1' for the first created
    # currency, 'ISO 2' for the next and so on

    iso_code = factory.Sequence(lambda n: 'ISO {0}'.format(n))
    title = factory.LazyAttribute(lambda a: '{0}'.format(a.iso_code))

class CurrencyRateFactory(factory.DjangoModelFactory):
    class Meta:
        model = CurrencyRate

    from_currency = factory.SubFactory(CurrencyFactory)
    to_currency = factory.SubFactory(CurrencyFactory)

class CurrencyRateHistoryFactory(factory.DjangoModelFactory):
    class Meta:
        model = CurrencyRateHistory

    rate = factory.SubFactory(CurrencyRateFactory)
    value = 0.89


def create_currencies():
    currency_eur = CurrencyFactory(iso_code='EUR')
    currency_usd = CurrencyFactory(iso_code='USD')
    currency_rate = CurrencyRateFactory(from_currency=currency_usd,
                                        to_currency=currency_eur)
    currency_history = CurrencyRateHistoryFactory(rate=currency_rate)
    return (currency_eur, currency_usd, currency_history)

