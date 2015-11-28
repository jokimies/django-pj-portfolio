# 3rd party
import factory
from django.test import TestCase

# Own
from portfolio.models import Security
from .security_factories import SecurityFactory

##########
#
# Tests
#
##########

class SecurityModelTest(TestCase):

    longMessage = True

    def create_security(self, name=None, ticker=None):
        """
        Create security
        If name is given, also assumes that ticker is given
        Returns security
        """

        if not name:
            return SecurityFactory()
        return SecurityFactory(name=name, ticker=ticker)
        
    def test_saving_security(self):

        security1 = self.create_security(name="Elisa", ticker="ELI1V")
        security2 = self.create_security()
        saved_items = Security.objects.all()
        self.assertEqual(saved_items.count(), 2,
                         'Should be two securities in db')

    def test_deleting_security(self):
        # First create a security
        self.create_security()
        security = Security.objects.latest('name')
        security.delete()
        security = Security.objects.filter(pk=security.pk)
        self.assertTrue(len(security) == 0)
