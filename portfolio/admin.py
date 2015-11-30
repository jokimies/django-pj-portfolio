from portfolio.models import Transaction, Security, Price, Account
from portfolio.models import PriceTracker
from django.contrib import admin

admin.site.register(Transaction)
admin.site.register(Security)
admin.site.register(Price)
admin.site.register(PriceTracker)
admin.site.register(Account)
