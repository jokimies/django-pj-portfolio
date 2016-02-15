# 3rd party

from django.core.urlresolvers import reverse
from django.utils import timezone

from rest_framework.test import APITestCase
from rest_framework import status

# Own
from .price_factories import PriceFactory
from .security_factories import SecurityFactory
from .account_base import AccountBase
from .currency_factories import create_currencies


class PositionApiTest(APITestCase, AccountBase):

    longMessage = True

    def setUp(self):

        self.account = self.create_account()
        self.security_name = 'Elisa'
        exchange_rate = 1
        security_amount = 100
        security_price = 22.5
        commission = 15

        # Currencies & rates
        currency_eur, self.currency_usd, self.rateHistory = create_currencies()
        security = SecurityFactory(name=self.security_name)
        self.elisa_price = PriceFactory(security=security,
                                        currency=currency_eur)

        self.account.buySellSecurity(security=security,
                                     shares=security_amount,
                                     date=timezone.now(),
                                     price=security_price,
                                     commission=commission, action='BUY',
                                     currency=currency_eur,
                                     exchange_rate=exchange_rate)

    def test_positions_api_returns_existing_position_list(self):

        response = self.client.get(
            reverse('positions',
                    kwargs={'account_id': self.account.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Checking the precence of all the fields
        data = response.data[self.security_name]
        self.assertIn('latest_date', data,
                      'Date missing from positions data')
        self.assertIn('total_return', data,
                      'Total return missing')
        self.assertIn('basis', data,
                      'Basis missing')
        self.assertIn('dividends', data,
                      'Dividends missing from positions data')
        self.assertIn('shares', data,
                      'Share count missing from data')
        self.assertIn('sold', data,
                      'Number of sold items missing from data')
        self.assertIn('average', data,
                      'Average price missing from data')
        self.assertIn('mktval', data,
                      'Market value missing from data')
        self.assertIn('gain', data,
                      'Gain missing from data')
        self.assertIn('change_percentage', data,
                      'Daily value change percentage missing from data')
        self.assertIn('folio_percentage', data,
                      'Weigth missing from data')
        self.assertIn('price', data,
                      'Item price missing from data')
        self.assertIn('change', data,
                      'Change in currency missong from data')
        self.assertEqual(len(data), 13,
                         'Item count does not match, added items?')
