from functools import partial
from recurly.models.base import BaseModel

class Account(BaseModel):
    """
    An account in Recurly correlates to a user in your application. Accounts /
    will automatically be created when creating a new subscription or /
    transaction. Alternatively, you may create an account at any time.
    """
    item_tag = 'account'
    collection_tag = 'accounts'
    known_attributes = (
        'account_code',
        'username',
        'email',
        'first_name',
        'last_name',
        'company_name',
        'balance_in_cents',
        'accept_language',
    )

    def __init__(self, *args, **kwargs):
        self.managed_class = ManagedAccount
        super(Account, self).__init__(*args, **kwargs)

    def __repr__(self):
        return "[Recurly Account: %r]" % self.account_code

class ManagedAccount(Account):
    def get_charges(self):
        return self._client.charges.get(self.account_code)

    def charge(self, amount_in_cents, description):
        return self._client.charges.post(self.account_code, amount_in_cents, description)

    def pending_charges(self):
        return self._client.charges.pending(self.account_code)

    def invoiced_charges(self):
        return self._client.charges.invoiced(self.account_code)

