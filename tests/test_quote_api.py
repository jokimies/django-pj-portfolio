try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

from django.core.urlresolvers import reverse

from rest_framework import status
#
from .currency_factories import create_currencies

MSFT_RESPONSE = {
    'date':'2018-10-19',
    'currency':'USD',
    'change':'0.16',
    'change_percentage':'0.147',
    'ticker':'MSFT',
    'price':'108.66'
}


class TestQuoteApi:

    @patch('portfolio.views.Command.get_alpha_vantage_stock_quote',
           return_value=MSFT_RESPONSE)
    def test_api_can_be_called(self, mock_av_quote, http_client):
        '''Test calling the API succeeds'''

        (currency_eur, currency_usd, currency_history) = create_currencies()
        # Replace currency with Currency object
        MSFT_RESPONSE['currency'] = currency_usd

        response = http_client.get(reverse('security-quote',
                                           kwargs={'stock': 'MSFT'}))
        assert response.status_code == status.HTTP_200_OK
