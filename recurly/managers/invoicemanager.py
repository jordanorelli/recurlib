from recurly import xmldict
from recurly.managers.base import BaseManager
from recurly.managers.decorators import autoparse

class InvoiceManager(BaseManager):
    endpoint = '/invoices'

    @autoparse
    def post(self, account_code):
        return self._client.post('/accounts/%s/invoices' % account_code)
