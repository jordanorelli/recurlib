from recurly.managers.base import BaseManager
from recurly.managers.decorators import autoparse

class AccountManager(BaseManager):
    """
    This class handles all of the API calls for Account objects.  You most
    likely don't want to instantiate it directly, as it is made available
    automatically when you create a Recurly API client and is exposed
    through a client instance's client.accounts member.
    """
    endpoint = '/accounts'

    @autoparse
    def all(self, page=None):
        if page:
            return self._client.get('/accounts?page=%s' % page)
        return self._client.get('/accounts')

    @autoparse
    def active(self):
        return self._client.get('/accounts?show=active_subscribers')

    @autoparse
    def past_due(self):
        return self._client.get('/accounts?show=pastdue_subscribers')

    @autoparse
    def non_subscribers(self):
        return self._client.get('/accounts?show=non_subscribers')

    @autoparse
    def get(self, account_code):
        return self._client.get('/accounts/%s' % account_code)
