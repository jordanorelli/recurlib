from recurly import xmldict
from recurly.managers.base import BaseManager
from recurly.managers.decorators import autoparse

class ChargeManager(BaseManager):
    @autoparse
    def get(self, account_code):
        """
        Lists all charges issued for a given account.
        """
        return self._client.get('/accounts/%s/charges' % account_code)

    @autoparse
    def post(self, account_code, amount_in_cents, description):
        if amount_in_cents < 0:
            raise ValueError(
                "Cowardly refusing to register a negative charge."
            )
        charge_data = xmldict('charge', {'amount_in_cents': amount_in_cents,
                                         'description': description})
        return self._client.post('/accounts/%s/charges' % account_code,
                                 data=charge_data)

    @autoparse
    def pending(self, account_code):
        """
        Lists all charges for a given account which have not been invoiced.
        """
        return self._client.get('/accounts/%s/charges?show=pending' % account_code)

    @autoparse
    def invoiced(self, account_code):
        """
        Lists all charges for a given account which have been invoiced.
        """
        return self._client.get('/account/%s/charges?show=invoiced' % account_code)
