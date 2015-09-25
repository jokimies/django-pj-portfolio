from django import forms
from portfolio.models import Security, Transaction, Account
from currency_history.models import Currency

class BuyForm(forms.ModelForm):

    #def __init__(self, *pa, **ka):
        #super(BuyForm, self).__init__(*pa, **ka)

        #self.fields['security'].queryset = Security.objects.all()


    class Meta:
        model = Transaction
        exclude = ['account', 'cash_amount', 'sec_fee', 'split_ratio', ]

class DepositWithdrawForm(forms.ModelForm):

    def __init__(self, *pa, **ka):
        super(DepositWithdrawForm, self).__init__(*pa, **ka)

        self.fields['security'].queryset = Security.objects.filter(name='$CASH')


    class Meta:
        model = Transaction
        exclude = ['account', 'action', 'shares', 'price', 'commission',
                   'sec_fee', 'split_ratio', ] 

class InterestForm(forms.Form):
    date = forms.DateField()
    amount = forms.DecimalField()

class DivForm(forms.ModelForm):
    class Meta:
        model = Transaction
        exclude = ['account', 'action', 'shares', 'sec_fee', 'split_ratio', ] 

class TxnBySecurityForm(forms.ModelForm):
    class Meta:
        model = Transaction
        exclude = ['account', 'action', 'shares', 'sec_fee', 'split_ratio', 
                   'cash_amount', 'commission', 'price', 'date', 
                   'currency', 'exchange_rate'] 

class AccountForm(forms.ModelForm):
    
    base_currency = forms.ModelChoiceField(queryset=Currency.objects.all(),initial={'base_currency':'USD'})

    class Meta:
        model = Account
        fields = ['name', 'base_currency']

class TransactionDetailForm(forms.ModelForm):
    
    class Meta:
        model = Transaction
        exclude = ['cash_amount', 'sec_fee', 'split_ratio']
