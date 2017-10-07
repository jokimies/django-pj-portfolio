# -*- coding: utf-8 -*-
# Standard imports
# For 2.x and 3.x compatibility
# (http://python-future.org/compatible_idioms.html)
from future.moves.urllib.request import urlopen
from future.moves.urllib.error import HTTPError

import json
import requests
from datetime import date
import re

# 3rd party imports
from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand

from currency_history.models import Currency

from bs4 import BeautifulSoup

# Own imports
from ...models import Security, Price


class Command(BaseCommand):

    soup = None

    def handle(self, **options):
        securities = Security.objects.all()
        today = date.today()

        for security in securities:
            if security.price_tracker.name == 'Kauppalehti':
                quote = self.get_kauppalehti_stock_quote(security.name)
            elif security.price_tracker.name == 'GoogleFinance':
                quote = self.get_google_finance_stock_quote(security.ticker)
            else:
                raise ImproperlyConfigured(
                    'Unkown price tracker {}'.format(
                        security.price_tracker.name))

            if not quote.get('price'):
                print('No ticker {} found by {}'.format(
                    security.ticker, security.price_tracker.name))
                continue
            # Check if there already is price for today
            try:
                Price.objects.filter(
                    security=security, date=today).latest('date')
            except Price.DoesNotExist:

                Price.objects.create(date=today, security=security,
                                     price=quote['price'],
                                     currency=quote['currency'],
                                     change=quote['change'],
                                     change_percentage=quote['change_percentage'])

    def get_google_finance_stock_quote(self, ticker_symbol):
        """
        """

        url = 'https://finance.google.com/finance?output=json&q=%s' % ticker_symbol
        response = requests.get(url)
        if response.status_code == 200:
            # This magic here is to cut out various leading characters from
            # the JSON response, as well as trailing stuff (a terminating
            # ']\n' sequence), and then we decode the escape sequences in
            # the response This then allows you to load the resulting
            # string with the JSON module.
            try:
                google_quote = json.loads(response.content[6:-2] \
                                          .decode('unicode_escape'))
            except ValueError:
                # The response does not start with b'\n// [\n{...', so it is
                # assumed that the query returned no matches, maybe something
                # like
                # b'\n{\n"start" : "",\n"num" : "",\n"num_company_results" :
                # "0",\n"num_mf_results" : "0",\n"num_all_results" : 
                # Return empty dictionary
                return {}
        else:
            # Something else was returned as response code than 200
            return {}

        quote = {}
        quote['price'] = google_quote['l']
        quote['change'] = google_quote['c'] or '0.0'
        quote['change_percentage'] = google_quote['cp'] or '0.0'

        # Get the currency, all stocks in Helsinki are expected to be in euros
        if google_quote['exchange'] == 'HEL':
            currency = Currency.objects.filter(
                iso_code='EUR')[0]
        else:
            currency = Currency.objects.filter(
                iso_code='USD')[0]
        quote['currency'] = currency
        return quote

    def get_kauppalehti_stock_quote(self, security_name):
        """
        Fetch stock quotes from Kauppalehti, by scraping the web page, as
        there's no API to get a quote for a single stock
        """

        quote = {}
        # Url to scrape
        url = "http://www.kauppalehti.fi/5/i/porssi/porssikurssit/lista.jsp?reverse=false&gics=kaikki&psize=300&rdc=117c1f2c2b5&currency=euro&listIds=kaikki&order=alpha&markets=XHEL"

        # Only fetch the web-page once
        if not self.soup:
            stock_page = urlopen(url)
            self.soup = BeautifulSoup(stock_page)

        # At the moment, 7th table has is the one with stock data
        table = self.soup('table')[6]

        # All prices are in Euros
        currency_euro = Currency.objects.filter(
            iso_code='EUR')[0]
        quote['currency'] = currency_euro

        for row in table.findAll('tr'):
            cells = row('td')

            # The table has headers inside <td>, but no need to worry about
            # them
            # First cell has the name of the stock
            if cells[0].a is not None:
                # Find the value inside <td> </td>
                if security_name == cells[0].a.string:
                    # Second cell has the current value of the stock
                    if cells[1] is not None:
                        quote['price'] = cells[1].string

                    # Change %
                    # Change percentage has '%' char at the end, remove it
                    # and convert  it to float. KL marks 'no change' as '-'
                    if cells[2].string == '-':
                        change_percentage = 0
                    else:
                        change_percentage = float(re.sub('[%]',
                                                         '',
                                                         cells[2].string))
                    # KL does not offer change in euros, need to calculate
                    current_value = float(cells[1].string)
                    previous_close = (current_value * 100) / (100 + change_percentage)
                    change = current_value - previous_close
                    quote['change'] = change
                    quote['change_percentage'] = change_percentage

        return quote
