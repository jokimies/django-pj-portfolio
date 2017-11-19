from django.core.urlresolvers import reverse

from rest_framework import status
#
from .currency_factories import create_currencies


class TestQuoteApi:

    def test_api_can_be_called(self, http_client):
        
        create_currencies()
        response = http_client.get(reverse('security-quote',
                                           kwargs={'stock': 'MSFT'}))
        assert response.status_code == status.HTTP_200_OK

    def test_api_return_some_content(self, http_client):
        '''Test the finance API is still working

        The actual code fecthing the quote data naturally uses external
        service, that might ahve stopped working for good. This test tries
        to catch those cases.
        '''

        create_currencies()

        response = http_client.get(reverse('security-quote',
                                           kwargs={'stock': 'MSFT'}))
        assert response.data is not {}
