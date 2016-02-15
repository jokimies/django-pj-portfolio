from django.conf.urls import patterns, url, include

#from rest_framework_nested import routers

from rest_framework.routers import DefaultRouter, SimpleRouter

from portfolio.views import *

router = SimpleRouter()
router.register(r'securities', SecurityViewSet)
router.register(r'accounts', AccountViewSet, 'api-account')

urlpatterns = patterns(
    '',
    url(r'^$', AccountListView.as_view(), name='account-list'),
    url(r'^account/(?P<pk>\d+)/$', AccountDetailView.as_view(), name='account-detail'),
    (r'^account/(?P<pk>\d+)/edit$', AccountEditView.as_view()),
    (r'^account/(?P<pk>\d+)/delete$', AccountDeleteView.as_view()),
    (r'^account/(?P<account_id>\d+)/deposit$', 'portfolio.views.deposit'),
    (r'^account/(?P<account_id>\d+)/withdraw$', 'portfolio.views.withdraw'),
    (r'^account/(?P<account_id>\d+)/transaction$', 'portfolio.views.buySell'),
    (r'^account/(?P<account_id>\d+)/div$', 'portfolio.views.div'),
    (r'^account/(?P<account_id>\d+)/interest$', 'portfolio.views.interest'),
    (r'^account/create$', AccountCreateView.as_view()),
    (r'^txn/all$', TransactionListView.as_view()),
    (r'^txn/(?P<account_id>\d+)/byname$', 'portfolio.views.txnByName'),
    (r'^txn/(?P<account_id>\d+)/byname/(?P<security_id>\d+)/$', TransactionListView.as_view()),
    (r'^txn/all/(?P<pk>\d+)/$', TransactionDetailView.as_view()),
    (r'^txn/(?P<account_id>\d+)/byname/(?P<security_id>\d+)/(?P<pk>\d+)/$', TransactionDetailView.as_view()),
    (r'^txn/create$', TransactionCreateView.as_view()),
    (r'^txn/(?P<pk>\d+)/delete$', TransactionDeleteView.as_view()),
    (r'^txn/(?P<account_id>\d+)/div$', 'portfolio.views.txnDiv'),
    (r'^txn/(?P<account_id>\d+)/(?P<action>div)/(?P<security_id>\d+)/$', DividendListView.as_view()),
    (r'^txn/(?P<account_id>\d+)/(?P<action>div)/(?P<security_id>\d+)/(?P<pk>\d+)/$', TransactionDetailView.as_view()),
    url(r'^txn/(?P<account_id>\d+)/divbyyear/(?P<year>[0-9]{4})/$', DividendYearListView.as_view(), name="divbyyear"), 
    url(r'^api/v1/', include(router.urls)),
    url(r'^securities/.*$', SecurityIndexView.as_view(), name='security-index'),
    url(r'^api/v1/transactions/dividend/(?P<year>[0-9]{4})/$',  DividendChartByYearView.as_view(), name='dividend-by-month-by-year'),
    #
    url(r'^api/v1/positions/(?P<account_id>\d+)/$', PositionView.as_view(), name='positions'),
)
