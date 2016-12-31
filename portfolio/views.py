import json
from decimal import Decimal
import datetime
import time

from django.db.models import Sum

from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, TemplateView
from django.utils.decorators import method_decorator


from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response


from portfolio.models import Transaction, Account, Security
from portfolio.forms import BuyForm, DepositWithdrawForm, InterestForm, DivForm, TxnBySecurityForm, AccountForm, TransactionDetailForm

from portfolio.serializers import SecuritySerializer, AccountSerializer


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, datetime.datetime):
            return obj.strftime ('%Y/%m/%d/%H/%M/%S')

        super(CustomEncoder, self).default(obj)


class PortfolioMixin(object):

    def get_account(self):
        account = get_object_or_404(Account, pk=account_id)
        return account

    def get_context_data(self, **kwargs):
        ctx = super(PortfolioMixin, self).get_context_data(**kwargs)
        ctx['account'] = self.get_account()
        #print ctx
        return ctx

class TransactionListView(ListView):
    model = Transaction

    # https://docs.djangoproject.com/en/dev/topics/class-based-views/generic-display/#dynamic-filtering
    def get_queryset(self):

        if 'action' in self.kwargs and 'security_id' in self.kwargs:
            return Transaction.objects.filter(security_id=self.kwargs['security_id']).filter(action=self.kwargs['action'].upper())
        elif 'security_id' in self.kwargs:
            return Transaction.objects.filter(security_id=self.kwargs['security_id'])
        else:
            return Transaction.objects.all()


class TransactionDetailView(UpdateView):
    model = Transaction
    form_class = TransactionDetailForm
    success_url = "/portfolio/txn/all"

class TransactionCreateView(CreateView):
    model = Transaction
    success_url = "/portfolio/txn/all"

class TransactionDeleteView(DeleteView):
    model = Transaction
    success_url = "/portfolio/txn/all"

class AccountListView(ListView):
    model = Account

class AccountDetailView(DetailView):
    model = Account

class AccountEditView(UpdateView):
    model = Account
    form_class = AccountForm
    success_url = "/portfolio"

class AccountCreateView(CreateView):
    model = Account
    form_class = AccountForm
    success_url = "/portfolio"

class AccountDeleteView(DeleteView):
    model = Account
    success_url = "/portfolio"

class DividendListView(ListView):
    model = Transaction
    template_name = "portfolio/dividend_list.html"

    # https://docs.djangoproject.com/en/dev/topics/class-based-views/generic-display/#dynamic-filtering
    def get_queryset(self):

        if 'action' in self.kwargs and 'security_id' in self.kwargs:
            return Transaction.objects.filter(security_id=self.kwargs['security_id']).filter(action=self.kwargs['action'].upper())
        elif 'security_id' in self.kwargs:
            return Transaction.objects.filter(security_id=self.kwargs['security_id'])

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(DividendListView, self).get_context_data(**kwargs)

        divsum = Transaction.objects.filter(account_id=self.kwargs['account_id']).filter(action='DIV').filter(security_id=self.kwargs['security_id']).aggregate(Sum('cash_amount'))
        context['divsum'] = divsum['cash_amount__sum']
        return context

class DividendYearListView(ListView):
    model = Transaction
    template_name = "portfolio/dividend_list.html"

    def get_queryset(self):

        return Transaction.objects.filter(date__year=self.kwargs['year']).filter(action='DIV')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(DividendYearListView, self).get_context_data(**kwargs)

        divsum = Transaction.objects.filter(date__year=self.kwargs['year']).filter(action='DIV').aggregate(Sum('cash_amount'))
        context['divsum'] = divsum['cash_amount__sum']
        context['year'] = self.kwargs['year']
        return context

class AccountViewSet(viewsets.ModelViewSet):
    """
    Returns list of accounts
    """

    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class SecurityViewSet(viewsets.ModelViewSet):
    """
    Returns a list of all securities.
    """

    queryset = Security.objects.all()
    serializer_class = SecuritySerializer
    permission_classes = [
        permissions.AllowAny
    ]

    def create(self, request):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            Security.objects.create_security(**serializer.validated_data)
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

        return Response({
            'status': 'Bad request',
            'message': 'Account could not be created with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)


class SecurityIndexView(TemplateView):
    template_name = 'security_index.html'

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, *args, **kwargs):
        return super(SecurityIndexView, self).dispatch(*args, **kwargs)

class DividendChartByYearView(APIView):

    def get(self, request, *args, **kwargs):
        bymonth_select = {"month": """DATE_TRUNC('month', date)"""} # Postgres specific
        months = Transaction.objects.extra(select=bymonth_select).filter(action='DIV').filter(date__year=self.kwargs['year']).values('month').annotate(sum_month=Sum('cash_amount')).order_by('month')
        div_data = {'months': list(range(1,13)), 'sums': [0]*12}

        for data in months:
            div_data['sums'][data['month'].month - 1] = data['sum_month']

        dataD = {}
        dataD['chart_data'] = div_data
        result = json.dumps(dataD, cls=CustomEncoder)
        
        response = Response(dataD, status=status.HTTP_200_OK) #, content_type='application/json')

        return response


class PositionView(APIView):
    """
    APIView to get positions for a certain account
    """

    def get(self, request, *args, **kwargs):
        """
        Get list of all positions

        - **parameters**, **return**::

          :param request: ``Request`` instance (from REST framework)
          :param kwargs: keyword parameters from URL, specifically ``account_id``
          :return: positions dictionary
        """

        account = get_object_or_404(Account, pk=kwargs['account_id'])

        data = account.positions()

        return Response(data, status=status.HTTP_200_OK)

# Functions


def deposit(request, account_id):
    a = get_object_or_404(Account, pk=account_id)
    if request.method == 'GET':
        form = DepositWithdrawForm()
    else:
        form = DepositWithdrawForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            security = form.cleaned_data['security']
            cash_amount = form.cleaned_data['cash_amount']
            currency = form.cleaned_data['currency']
            a.deposit(cash_amount=cash_amount, date=date, security=security,
                      currency=currency)
            return redirect('/portfolio/account/' + account_id + '/')
    action_title = "Deposit"
    title = action_title + " cash"
    return render(request, 'portfolio/deposit_withdraw.html', 
                  {'form': form,
                   'title': title,
                   'action_title': action_title,})

def withdraw(request, account_id):
    a = get_object_or_404(Account, pk=account_id)
    if request.method == 'GET':
        form = DepositWithdrawForm()
    else:
        form = DepositWithdrawForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            security = form.cleaned_data['security']
            cash_amount = form.cleaned_data['cash_amount']
            currency = form.cleaned_data['currency']
            a.withdraw(cash_amount=cash_amount, date=date, security=security,
                       currency=currency)
            return redirect('/portfolio/account/' + account_id + '/')
    action_title = "Withdraw"
    title = action_title + " cash"
    return render(request, 'portfolio/deposit_withdraw.html', 
                  {'form': form,
                   'title': title,
                   'action_title': action_title,})

def buySell(request, account_id):
    a = get_object_or_404(Account, pk=account_id)
    if request.method == 'GET':
        form = BuyForm()
    else:
        form = BuyForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            security = form.cleaned_data['security']
            shares = form.cleaned_data['shares']
            price = form.cleaned_data['price']
            action = form.cleaned_data['action']
            commission = form.cleaned_data['commission']
            currency = form.cleaned_data['currency']
            exchange_rate = form.cleaned_data['exchange_rate']
            a.buySellSecurity(security=security, shares=shares, date=date,
                              price=price, commission=commission, action=action,
                              currency=currency, exchange_rate=exchange_rate)
            return redirect('/portfolio/account/' + account_id + '/')
    return render(request, 'portfolio/transaction.html', 
                  {'form': form,
                   'account': a,
                   'sub_title': 'Buy or sell'})

def div(request, account_id):
    a = get_object_or_404(Account, pk=account_id)
    if request.method == 'GET':
        form = DivForm()
    else:
        form = DivForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            security = form.cleaned_data['security']
            price = form.cleaned_data['price']
            commission = form.cleaned_data['commission']
            cash_amount = form.cleaned_data['cash_amount']
            currency = form.cleaned_data['currency']
            exchange_rate = form.cleaned_data['exchange_rate']
            a.div(security=security, date=date,
                  price=price, commission=commission, 
                  cash_amount=cash_amount,
                  currency=currency, exchange_rate=exchange_rate)
            return redirect('/portfolio/account/' + account_id + '/')
    return render(request, 'portfolio/transaction.html', 
                  {'form': form,
                   'account': a,
                   'sub_title': 'Add dividends',})

def txnByName(request, account_id):
    a = get_object_or_404(Account, pk=account_id)
    if request.method == 'GET':
        form = TxnBySecurityForm()
    else:
        form = TxnBySecurityForm(request.POST)
        if form.is_valid():
            security = form.cleaned_data['security']
            a.txnByName(security=security)
        return redirect('/portfolio/txn/' + account_id + '/byname/' + str(security.id) + '/')
    return render(request, 'portfolio/transaction.html', 
                  {'form': form,
                   'account': a,
                   'sub_title': 'Transactions by security'})

def txnDiv(request, account_id):
    a = get_object_or_404(Account, pk=account_id)
    if request.method == 'GET':
        form = TxnBySecurityForm()
        years = Account.div_years.div_years(account_id)
    else:
        form = TxnBySecurityForm(request.POST)
        if form.is_valid():
            security = form.cleaned_data['security']

            sum = Transaction.objects.filter(account_id=account_id).filter(action='DIV').filter(shares__gt=0).aggregate(Sum('cash_amount'))
            
        return redirect('/portfolio/txn/' + account_id + '/div/' + str(security.id) + '/')
    return render(request, 'portfolio/transaction.html', 
                  {'form': form,
                   'yearly_divs' : True,
                   'years' : years,
                   'account' : a,
                   'sub_title': 'Display dividends'})


def interest(request, account_id):
    a = get_object_or_404(Account, pk=account_id)
    if request.method == 'GET':
        form = InterestForm()
    else:
        form = InterestForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            amount = form.cleaned_data['amount']
            a.receive_interest(amount=amount, date=date)
            return redirect('/portfolio/account/' + account_id + '/')
    return render(request, 'portfolio/interest.html', {'form': form})
