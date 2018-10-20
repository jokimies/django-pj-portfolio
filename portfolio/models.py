# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from collections import defaultdict
from decimal import Decimal

#
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible

from currency_history.models import Currency, CurrencyRate

import time

class DivManager(models.Manager):
    """Dividends manager to return all the years dividends have been received
    
    """
    def div_years(self, account_id):
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("""
        select EXTRACT(YEAR FROM date) as year from
        portfolio_transaction where action = 'DIV' and
        account_id=%s group by year order
        by year""", (account_id) )
        #years = cursor.fetchall()
        desc = cursor.description
        years = [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
        ]

        return years

@python_2_unicode_compatible
class Account(models.Model):
    name = models.CharField(max_length=50)
    base_currency = models.CharField(verbose_name=_('Base currency,ISO-code'),
                                     max_length=3, unique=False,
                                     default='EUR')
                                     
    positions = {}
    div_years = DivManager()
    # Setting DivManager above causes django to drop default manager. Needs
    # to be added back
    objects = models.Manager()


    def __init__(self, *args, **kwargs):
        models.Model.__init__(self, *args, **kwargs)
        self.positions = {'$CASH': self.new_position() }

    def buySellSecurity(self, security=None, shares=None, date=None,
                        price=None, commission=0, action=None, currency=None,
                        exchange_rate=None):
        t = Transaction()
        t.account = self
        t.action = action
        t.security = security
        t.shares = Decimal(shares)
        t.date = date
        t.price = Decimal(price)
        t.commission = Decimal(commission)
        t.currency = currency
        t.exchange_rate = exchange_rate
        t.save()

    def div(self, security=None, date=None, price=None, commission=0,
            cash_amount=0, currency=None, exchange_rate=None):
        t = Transaction()
        t.account = self
        t.action = 'DIV'
        t.security = security
        t.date = date
        t.price = Decimal(price)
        #t.commission = Decimal(commission)
        t.cash_amount = Decimal(cash_amount)
        t.currency = currency
        t.exchange_rate = exchange_rate
        t.save()

    def txnByName(self, security=None):
        print ("{} {}".format(security.name, security.id))

    # def sell_security(self, security=None, shares=None, date=None,
    #                   price=None, commission=0, sec_fee=0):
    #     t = Transaction()
    #     t.account = self
    #     t.action = 'SELL'
    #     t.security = 1
    #     t.shares = Decimal(shares)
    #     t.date = date
    #     t.price = Decimal(price)
    #     t.commission = Decimal(commission)
    #     t.sec_fee = Decimal(sec_fee)
    #     t.save()

    #     Price.objects.create(date=date, security=security,
    #                          price=price)

    # def dividend(self, security=None, amount=0.00, date=None):
    #     t = Transaction()
    #     t.account = self
    #     t.action = 'DIV'
    #     t.security = security
    #     t.date = date
    #     t.cash_amount = Decimal(amount)
    #     t.save()

    def deposit(self, cash_amount=0, date=None, security=None, currency=None):
         t = Transaction()
         t.account = self
         t.action = 'DEP'
         t.cash_amount = Decimal(cash_amount)
         t.date = date
         t.security = security
         t.currency = currency
         t.save()

    def withdraw(self, cash_amount=0, date=None, security=None, currency=None):
         t = Transaction()
         t.account = self
         t.action = 'WITH'
         t.cash_amount = Decimal(-cash_amount)
         t.date = date
         t.security = security
         t.currency = currency
         t.save()

    # def receive_interest(self, amount=0, date=None):
    #     t = Transaction()
    #     t.account = self
    #     t.action = 'INT'
    #     t.cash_amount = Decimal(amount)
    #     t.date = date
    #     t.save()

    # def pay_interest(self, amount=0, date=None):
    #     t = Transaction()
    #     t.account = self
    #     t.action = 'MARGIN'
    #     t.cash_amount = Decimal(-amount)
    #     t.date = date
    #     t.save()

    # def stock_split(self, security=None, split_ratio=0, date=None):
    #     t = Transaction()
    #     t.account = self
    #     t.action = 'SS'
    #     t.security = security
    #     t.split_ratio = split_ratio
    #     t.date = date
    #     t.save()

    def new_position(self):
        return dict(shares=0, price=1, basis=0,
                    mktval=0, gain=0, dividends=0, average=0,
                    total_return=0, sold=0)

    def update_market_value(self, positions, date):

        for security in positions:
            p = positions[security]
            if security == '$CASH':
                price = 1.00
                from_currency = self.base_currency
            else:
                latest_price = Price.objects.select_related('currency').filter(
                    security__name=security, date__lte=date).latest('date')
                price = latest_price.price

                # What is the currency used for this security
                from_currency = latest_price.currency.iso_code

                # Store change compared to previous close
                positions[security]['change'] = latest_price.change

                # Also change percentage
                positions[security]['change_percentage'] = latest_price.change_percentage
                positions[security]['latest_date'] = latest_price.date

            # Prepare for converting currency in Price for the security to
            # base_security
            if from_currency == self.base_currency:
                exchange_rate = 1.0
            else:
                rate = CurrencyRate.objects.get(
                    from_currency__iso_code=from_currency,
                    to_currency__iso_code=self.base_currency)
                history = rate.history.all()[0]
                exchange_rate = history.value

            mktval = p['shares'] * Decimal(price) * Decimal(exchange_rate)
            gain = mktval - p['basis'] + p['sold'] + p['dividends']
            if p['basis']:
                tr = ((mktval + p['sold'] + p['dividends']) / p['basis'] - 1) * 100
                positions[security]['total_return'] = tr

            positions[security]['mktval'] = mktval
            positions[security]['gain'] = gain
            positions[security]['price'] = price

        folio_mktval = self.mktval()
        for security in positions:
            # skip cash
            if security == '$CASH':
                continue
            p = positions[security]
            positions[security]['folio_percentage'] = (p['mktval'] / folio_mktval ) * 100
        return positions

    def get_positions(self, date=None):
        """Return a dictionary of all of the positions in this account.

        If date is provided, then only include transactions up to (and
        including) that date."""

        # list of buys of one share
        buyStack = []
        # Dictionary of list containing all buys
        shareTransaction = defaultdict(list)
        # 
        buyDict = {}
        if not date:
            date = timezone.now()
        positions = {'$CASH': self.new_position()}
        #positions = {}
        transactions = Transaction.objects.select_related('security').filter(
            account=self, date__lte=date).order_by('date', 'id')
        for t in transactions:
            if  t.security.name and t.security.name not  in positions:
                positions[t.security.name] = self.new_position()
            # switch based on transaction action
            if t.action in ('DEP', 'WITH'):
                positions['$CASH']['basis'] += t.cash_amount
                positions['$CASH']['shares'] += t.cash_amount
            elif t.action in ('INT', 'MARGIN'):
                positions['$CASH']['shares'] += t.cash_amount
            elif t.action == 'DIV':
                positions['$CASH']['basis'] += t.cash_amount
                positions['$CASH']['shares'] += t.cash_amount
                positions[t.security.name]['dividends'] += t.cash_amount
            elif t.action == 'SS':
                positions[t.security.name]['shares'] *= t.split_ratio
            elif t.action == 'BUY':
                positions[t.security.name]['basis'] += (
                    t.shares * t.price * t.exchange_rate + t.commission)
                positions[t.security.name]['shares'] += t.shares
                cost = t.shares * (t.price * t.exchange_rate) + t.commission
                positions['$CASH']['basis'] -= cost
                positions['$CASH']['shares'] -= cost

                # Put the bought batch into list, stored in dictionary for
                # this share (Dictionary of list of dictionaries)
                shareTransaction[t.security.name].append({ 'shares' : t.shares, 'price' : t.price })
            elif t.action == 'SELL':
                # Collect list of current holdings: how many is left at the
                # price those were boughtfor

                buyList = shareTransaction[t.security.name].pop()
                #if t.security.name ==  u'Ilkka-Yhtymä II':
                #    print "%s %d " % (t.security.name, t.shares)
                #    print "Popped"
                #    print shareTransaction[t.security.name]
                #    print buyList
                sold = t.shares
                moreToSell = True
                
                # is more being sold that the current bought batch
                if sold >= buyList['shares']:
                    while moreToSell:
                        # How many needs to be taken from next batch
                        sold = sold - buyList['shares']

                        # Try to prevent floating point precision errors
                        # code here

                        # If stack is empty, ie all shares sold, break out of
                        # the loop
                        if not  shareTransaction[t.security.name]:
                            break
                        # next item from array
                        buyList = shareTransaction[t.security.name].pop()
                        if sold < buyList['shares']:
                            moreToSell = False
                    else: # while condition false
                        buyList['shares'] = buyList['shares'] - sold
                        if buyList['shares'] > 0:
                            shareTransaction[t.security.name].append(buyList)
                else:
                    buyList['shares'] = buyList['shares'] - sold
                    if buyList['shares'] > 0:
                        shareTransaction[t.security.name].append(buyList)

                ##
                current_shares = positions[t.security.name]['shares']
                if current_shares:
                    old_basis_ps = (positions[t.security.name]['basis'] /
                                    positions[t.security.name]['shares'])
                    positions[t.security.name]['shares'] -= t.shares
                    positions[t.security.name]['sold'] += t.shares * (t.price * t.exchange_rate)

                else:
                    old_basis_ps = t.price
                    positions[t.security.name]['basis'] -= old_basis_ps * t.shares
                    #positions[t.security.name]['shares'] -= t.shares
                positions['$CASH']['basis'] += t.shares * (t.price * t.exchange_rate) - t.commission
                positions['$CASH']['shares'] += t.shares * (t.price * t.exchange_rate)  - t.commission

        # Calculate avegare prices per share to be sold
        for key in shareTransaction:
            average = 0
            cost = 0
            count = 0
            for transaction in shareTransaction[key]:
                count += transaction['shares']
                cost += transaction['price'] * transaction['shares']
                if count:
                    average = cost / count
                    positions[key]['average'] = average

        self.positions = positions
        return self.update_market_value(positions, date)

    def mktval(self, security=None):
        positions = self.positions

        if security:
            return positions[security]['mktval']
                #for p in positions:
        #    print "%s %d " % (p,positions[p]['mktval'])

        #print sum(positions[p]['mktval'] for p in positions)
                #if any(positions):
        return sum(positions[p]['mktval'] for p in positions)
     
    def basis(self, security=None):
        positions = self.positions
        if security:
            return positions[security]['basis']
        return sum(positions[p]['basis'] for p in positions)

    def sells(self, security=None):
        positions = self.positions
        if security:
            return positions[security]['sold']
        return sum(positions[p]['sold'] for p in positions)
        
    def gain(self, security=None):
        positions = self.positions
        if security:
            return positions[security]['gain']
        return sum(positions[p]['gain'] for p in positions)

    def dividends(self, security=None):
        positions = self.positions
        if security:
            return positions[security]['dividends']
        return sum(positions[p]['dividends'] for p in positions)

    def total_return(self, security=None):
        positions = self.positions
        if security:
            return positions[security]['total_return']
        if self.basis():
            return ((self.mktval() + self.dividends() + self.sells()) / self.basis() - 1) * 100

    @property
    def cash(self):
         positions = self.positions
         return positions['$CASH']

    def __str__(self):
        return self.name


class SecurityManager(models.Manager):

    def create_security(self, name, ticker):
        if not name:
            raise ValueError('Security must have name.')

        if not ticker:
            raise ValueError('Security must have ticker.')

        security = self.model(
            name=name, 
            ticker=ticker,
        )
        security.save()
        return security

@python_2_unicode_compatible
class PriceTracker(models.Model):
    """
    Site to get security prices from
    """
    name = models.CharField(max_length=40, blank=False)

    def __str__(self):
        return self.name

def set_default_tracker():
    """
    Set default tracker to Kauppalehti for new Securities
    """ 
    tracker, created = PriceTracker.objects.get_or_create(name='Kauppalehti')
    return tracker.pk

@python_2_unicode_compatible
class Security(models.Model):
    ticker = models.CharField(max_length = 40, blank=False)
    name = models.CharField(max_length = 40, blank=False)
    price_tracker = models.ForeignKey(PriceTracker, default=set_default_tracker)

    objects = SecurityManager()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name + ' ' + self.ticker

@python_2_unicode_compatible
class Price(models.Model):
    date = models.DateField('transaction date')
    security = models.ForeignKey(Security)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    currency = models.ForeignKey(Currency)
    change = models.DecimalField(decimal_places=2, max_digits=6, 
                               blank=True, null=True)
    change_percentage = models.DecimalField(decimal_places=2, max_digits=6,
                               blank=True, null=True)

    def __str__(self):
        return self.security.name + ' ' + str(self.date) + ' ' + str(self.price)


TRANSACTION_CHOICES = (
    ('BUY', 'Buy'),
    ('SELL', 'Sell'),
)

@python_2_unicode_compatible
class Transaction(models.Model):
    account = models.ForeignKey(Account)
    action = models.CharField(max_length=10, choices=TRANSACTION_CHOICES)
    date = models.DateField('transaction date')
    security = models.ForeignKey(Security)
    shares = models.DecimalField(decimal_places=4, max_digits=10, null=True)
    currency = models.ForeignKey(Currency)
    exchange_rate = models.DecimalField(decimal_places=4, max_digits=10,
    null=False, blank=False, default=Decimal('1.0'))
    price = models.DecimalField(decimal_places=4, max_digits=10, null=True)
    commission = models.DecimalField(decimal_places=2, max_digits=10,
                                     null=True)
    cash_amount = models.DecimalField(decimal_places=2, max_digits=10,
                                      null=True)
    sec_fee = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    split_ratio = models.DecimalField(decimal_places=2, max_digits=5,
                                      null=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.action + ' ' + str(self.shares) + ' ' + self.security.name

