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


class AccountApiTest(APITestCase, AccountBase):

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

    def test_account_api_returns_existing_account_list(self):
        """
        Check the account api returns existing accounts
        """

        response = self.client.get(
            reverse('api-account-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for account in response.data:
            # Account should have name
            self.assertTrue(account['name'])
