from recurly.models.base import BaseModel
from xml.etree.cElementTree import Element, tostring

class Account(BaseModel):
    """
    An account in Recurly correlates to a user in your application. Accounts /
    will automatically be created when creating a new subscription or /
    transaction. Alternatively, you may create an account at any time.
    """
    item_tag = 'account'
    collection_tag = 'accounts'
    pk_attrib = 'account_code'
    managed_class = 'ManagedAccount'
    known_attributes = (
        'id',
        'account_code',
        'username',
        'email',
        'first_name',
        'last_name',
        'company_name',
        'balance_in_cents',
        'accept_language',
    )

    def __repr__(self):
        return "[Recurly Account: %r]" % self.account_code

class ManagedAccount(Account):
    known_attributes = Account.known_attributes + (
        'closed',
        'hosted_login_token',
        'created_at',
        'state',
    )

    def get_charges(self):
        """
        Lists all charges issued for a given account.
        """
        return self._client.charges.get(self.account_code)

    def charge(self, amount_in_cents, description):
        """
        Creates a one-time charge on an account.  Charges are not invoiced or
        collected immediately.  Uninvoiced charges will automatically be
        invoiced when the account's subscription renews, or you trigger a
        collection by posting an invoice.  Charges may be removed from an
        account if they have not been invoiced.
        """
        return self._client.charges.post(self.account_code,
                                         amount_in_cents,
                                         description)

    def invoice(self):
        """
        When you post one-time charges to an account, these will remain
        pending until they are invoiced.  An account is automatically
        invoiced when the subscription renews.  However, there are times when
        it is appropriate to invoice an account before the renewal.  If the
        subscriber has a yearly subscription, you might want to collect the
        one-time charges well before the renewal.
        """
        return self._client.invoices.post(self.account_code)

    def pending_charges(self):
        """
        Lists all charges for this account which have not been invoiced.
        """
        return self._client.charges.pending(self.account_code)

    def invoiced_charges(self):
        """
        Lists all charges for this account which have been invoiced.
        """
        return self._client.charges.invoiced(self.account_code)

