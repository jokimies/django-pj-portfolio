
# Django
from django.core.urlresolvers import reverse

# Own
from .account_base import AccountTestCase

class AccountHomePageTest(AccountTestCase):
    
    def test_account_home_page_renders_accout_detail_template(self):
        response = self.client.get(reverse('account-detail', args=(self.account.id,)))
        self.assertTemplateUsed(response, 'portfolio/account_detail.html')


