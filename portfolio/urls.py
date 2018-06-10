from django.conf.urls import url, include

#from rest_framework_nested import routers

from rest_framework.routers import DefaultRouter, SimpleRouter

from portfolio.views import *
from portfolio import views as portfolio_views

router = SimpleRouter()
router.register(r'securities', SecurityViewSet)
router.register(r'accounts', AccountViewSet, 'api-account')

urlpatterns = [
    url(r'^$', AccountListView.as_view(), name='account-list'),
    url(r'^account/(?P<pk>\d+)/$', AccountDetailView.as_view(), name='account-detail'),
    url(r'^account/(?P<pk>\d+)/edit$', AccountEditView.as_view()),
    url(r'^account/(?P<pk>\d+)/delete$', AccountDeleteView.as_view()),
    url(r'^account/(?P<account_id>\d+)/deposit$', deposit),
    url(r'^account/(?P<account_id>\d+)/withdraw$', withdraw),
    url(r'^account/(?P<account_id>\d+)/transaction$', buySell),
    url(r'^account/(?P<account_id>\d+)/div$', div),
    url(r'^account/(?P<account_id>\d+)/interest$', interest),
    url(r'^account/create$', AccountCreateView.as_view()),
    url(r'^txn/all$', TransactionListView.as_view()),
    url(r'^txn/(?P<account_id>\d+)/byname$', txnByName),
    url(r'^txn/(?P<account_id>\d+)/byname/(?P<security_id>\d+)/$',
        TransactionListView.as_view()),
    url(r'^txn/all/(?P<pk>\d+)/$', TransactionDetailView.as_view()),
    url(r'^txn/(?P<account_id>\d+)/byname/(?P<security_id>\d+)/(?P<pk>\d+)/$',
        TransactionDetailView.as_view()),
    url(r'^txn/create$', TransactionCreateView.as_view()),
    url(r'^txn/(?P<pk>\d+)/delete$', TransactionDeleteView.as_view()),
    url(r'^txn/(?P<account_id>\d+)/div$', portfolio_views.txnDiv),
    url(r'^txn/(?P<account_id>\d+)/(?P<action>div)/(?P<security_id>\d+)/$',
        DividendListView.as_view()),
    url(r'^txn/(?P<account_id>\d+)/(?P<action>div)/(?P<security_id>\d+)/(?P<pk>\d+)/$', TransactionDetailView.as_view()),
    url(r'^txn/(?P<account_id>\d+)/divbyyear/(?P<year>[0-9]{4})/$',
        DividendYearListView.as_view(), name="divbyyear"), 
    url(r'^api/v1/', include(router.urls)),
    url(r'^securities/.*$', SecurityIndexView.as_view(), name='security-index'),
    url(r'^api/v1/transactions/dividend/(?P<year>[0-9]{4})/$',
        DividendChartByYearView.as_view(), name='dividend-by-month-by-year'),
    #
    url(r'^api/v1/positions/(?P<account_id>\d+)/$', PositionView.as_view(),
        name='positions'),
    url(r'^api/v1/(?P<stock>.*)/quote/', SecurityQuoteView.as_view(),
        name='security-quote'),
    url(r'^api/v1/exchange/', ExchangeRatesView.as_view(),
        name='exchange-rates'),
]
