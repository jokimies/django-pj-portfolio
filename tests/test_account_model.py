from decimal import Decimal

# 3rd party
from django.test import TestCase
from django.utils import timezone


# Own

from .security_factories import SecurityFactory
from .price_factories import PriceFactory
from .currency_factories import *
from .account_base import AccountBase


from portfolio.models import Account

    
class AccountModelTest(AccountBase, TestCase):

    longMessage = True


    def setUp(self):
        self.account = self.create_account()
        self.account.save()

        # Currencies & rates
        self.currency_eur, self.currency_usd, self.rateHistory = create_currencies()
        self.security = SecurityFactory(name='Elisa')
        self.elisa_price = PriceFactory(security=self.security, 
                                        currency=self.currency_eur)
        self.security_cash = SecurityFactory(name='$CASH')

    def test_saving_account(self):
        self.create_account()
        self.create_account()
        saved_items = Account.objects.all()
        # 3 accounts should be found: the two created above, and the on
        # created in setUP
        self.assertEqual(saved_items.count(), 3,
                         'Should be three securities in db')

    def test_edit_base_currency(self):

        account = Account.objects.latest('name')
        account.base_currency = 'USD'
        account.save()

        edited_base_currency = Account.objects.get(pk=account.pk)

        self.assertEqual(edited_base_currency.base_currency, 'USD')

    def test_deposit(self):
        self.account.deposit(cash_amount=1000.12, date=timezone.now(),
                             security=self.security_cash, currency=self.currency_eur)
        positions = self.account.get_positions()
        self.assertEquals(positions['$CASH']['shares'], Decimal('1000.12'))
        
    def test_withdraw(self):
        self.account.deposit(cash_amount=1000.12, date=timezone.now(),
                             security=self.security, currency=self.currency_eur)

        self.account.withdraw(cash_amount=90, date=timezone.now(),
                              security=self.security, currency=self.currency_eur)
        positions = self.account.get_positions()
        # 'Converting' 1000.12 - 90 to contain 2 decimals 
        #self.assertEquals(positions['$CASH']['shares'], Decimal('%.2f' % (1000.12 - 90)))

    def buy_security(self, exchange_rate=1, security_amount=100, 
                         security_price=22.5, commission=15, cash_amount=3000.12):
        # First, store some money
        self.account.deposit(cash_amount=cash_amount, date=timezone.now(),
                             security=self.security_cash, 
                             currency=self.currency_eur)

        self.account.buySellSecurity(security=self.security, 
                                     shares=security_amount, 
                                     date=timezone.now(), 
                                     price=security_price,
                                     commission=commission, action='BUY',
                                     currency=self.currency_eur,
                                     exchange_rate=exchange_rate)
        positions = self.account.get_positions()
        # Should be as many in possession as bought above
        self.assertEquals(positions[self.security.name]['shares'], security_amount)
        # How much there's cash?
        cost = security_amount * (security_price * float(exchange_rate)) + commission
        #print positions['$CASH']['shares'], positions[self.security.name]['shares'], positions[self.security.name]['mktval'], 

        self.assertEquals(positions['$CASH']['shares'], 
                          Decimal('%.2f' % (cash_amount - cost)))


    def test_buy_security(self):
        self.buy_security(exchange_rate=1)

    def test_buy_more_securities(self):
    
        first_buy_security_amount = 100
        first_buy_security_price = 22.5
        second_buy_security_amount = 150
        second_buy_security_price = 20.21
        
        total_buy_amount = first_buy_security_amount + second_buy_security_amount
        commission = 15
        cash_amount = 5000.12
        
        exchange_rate = 1
        first_buy_cost = first_buy_security_amount * first_buy_security_price + commission
        second_buy_cost = second_buy_security_amount * second_buy_security_price + commission
        total_cost = first_buy_cost + second_buy_cost

        # First, store some money
        self.account.deposit(cash_amount=cash_amount, date=timezone.now(),
                             security=self.security_cash, 
                             currency=self.currency_eur)

        # Then buy
        self.account.buySellSecurity(security=self.security, 
                                     shares=first_buy_security_amount, 
                                     date=timezone.now(), 
                                     price=first_buy_security_price,
                                     commission=commission, action='BUY',
                                     currency=self.currency_eur,
                                     exchange_rate=exchange_rate)
        
        self.account.buySellSecurity(security=self.security, 
                                     shares=second_buy_security_amount, 
                                     date=timezone.now(), 
                                     price=second_buy_security_price,
                                     commission=commission, action='BUY',
                                     currency=self.currency_eur,
                                     exchange_rate=exchange_rate)

        positions = self.account.get_positions()
        # Should be as many in possession as bought above
        self.assertEquals(positions[self.security.name]['shares'], total_buy_amount)
        # And the cash?
        self.assertEquals(positions['$CASH']['shares'], 
                          Decimal('%.2f' % (cash_amount - total_cost)))

    def test_buy_security_foreign_currency(self):
        self.buy_security(exchange_rate=0.8)


    def sell_security(self, exchange_rate=1):
        cash_amount = 5000
        buy_amount = 200
        buy_price = 19.80
        commission = 15

        cost = buy_amount * ( buy_price * float(exchange_rate) )  + commission

        sell_amount = 190
        sell_price = 19.90
        sell_commission = 16

        sell_yield = sell_amount * ( sell_price * float(exchange_rate)) - sell_commission
        remaining_cash = cash_amount - cost + sell_yield

        # First, store some money
        self.account.deposit(cash_amount=cash_amount, date=timezone.now(),
                             security=self.security_cash, currency=self.currency_eur)

        # Then buy
        self.account.buySellSecurity(security=self.security, 
                                     shares=buy_amount, 
                                     date=timezone.now(), 
                                     price=buy_price,
                                     commission=commission, action='BUY',
                                     currency=self.currency_eur,
                                     exchange_rate=exchange_rate)
        # And sell
        self.account.buySellSecurity(security=self.security, 
                                     shares=sell_amount, 
                                     date=timezone.now(), 
                                     price=sell_price,
                                     commission=sell_commission, action='SELL',
                                     currency=self.currency_eur,
                                     exchange_rate=exchange_rate)
        
        positions = self.account.get_positions()

        # Corrent amount of shares left?
        self.assertEquals(positions[self.security.name]['shares'],
                          buy_amount - sell_amount)

        # And cash?
        self.assertEquals(positions['$CASH']['shares'], 
                          Decimal('%.2f' % remaining_cash))


    def test_sell_security(self):
        self.sell_security(exchange_rate=1)


    def test_sell_security_foreign_currency(self):
        self.sell_security(exchange_rate=0.8)

    def test_dividend(self):
        """ 
        Test adding dividend. Dividend sum is always entered in EURos
        """
        
        dividend_sum = 231.76
        self.account.div(security=self.security, price=1.3,
                         cash_amount=dividend_sum, date=timezone.now(), 
                         currency=self.currency_eur, exchange_rate=1)

        positions = self.account.get_positions()
        # How much do we have
        self.assertEquals(positions['$CASH']['shares'], 
                          Decimal('%.2f' % dividend_sum))


    def test_market_value(self):

        current_price=18.00
        security_amount = 100
        security_price = 10
        cash_amount = 1000
        commission = 15
        buy_exchange_rate = 0.91
        exchange_rate_usd_eur = self.rateHistory.value

        self.security = SecurityFactory(name='MORL')
        self.morlprice = PriceFactory(security=self.security, price=current_price, currency=self.currency_usd)

        self.buy_security(exchange_rate=buy_exchange_rate,
                          security_amount=security_amount,
                          security_price=security_price,
                          commission=commission, cash_amount=cash_amount)

        cost = security_amount * (security_price * float(buy_exchange_rate)) + commission

        # Expected value: cash - cost of purchase + the current value of
        # the bought stocks, current exchange rate taken into account.. not
        # the one rate happened to be at the time of buying
        expected_value = cash_amount - cost + security_amount * current_price * exchange_rate_usd_eur
        self.assertEquals(Decimal('%.2f' % (self.account.mktval())), 
                          Decimal('%.2f' % (expected_value)))


    def test_market_value_no_securities_is_bought(self):
        
        positions = self.account.get_positions()
        self.account.mktval()

    def test_overall_return(self):
        pass
