
## Django
from django.test import TestCase

# Own
from .account_factories import AccountFactory

class AccountTestCase(TestCase):

    def create_account(self, name=None):
        """
        Create an account

        Inputs: name - name for the account. If not given uses default
        defined by factory

        Returns created account
        """

        if not name:
            return AccountFactory()

        return AccountFactory(name=name)

    def setUp(self):
        
        self.account = self.create_account('MyAccount')
