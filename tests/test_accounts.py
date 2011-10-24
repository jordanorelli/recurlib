#!/usr/bin/env python
import unittest
from random import choice
from string import letters, digits
from credentials import credentials as creds
from recurly.client import Client
from recurly.models import Account, ManagedAccount, Charge, Invoice
from recurly.exceptions import RecurlyNotFoundException, RecurlyException

def randomstring(length):
    return ''.join([choice(letters+digits) for x in range(length)])

class AccountTest(unittest.TestCase):

    def setUp(self):
        self.client = Client(
            creds['subdomain'],
            creds['api_key'],
            creds['private_key'],
        )
        self.account_data = {
            'account_code': randomstring(8),
            'username': randomstring(8),
            'first_name': randomstring(8),
            'last_name': randomstring(8),
            # 'email': randomstring(8) + '@example.com',
            'company_name': randomstring(8),
        }

    def test_accounts(self):
        # make sure it's not there.
        self.assertRaises(
            RecurlyNotFoundException,
            self.client.accounts.get,
            self.account_data['account_code'],
        )

        # create an account
        account = Account(**self.account_data)
        created = self.client.accounts.create(account)
        self.assertTrue(isinstance(created, ManagedAccount))

        # check the accounts attributes
        for k, v in self.account_data.items():
            self.assertEqual(getattr(created, k), v)

        # make sure you can retrieve the account
        fetched = self.client.accounts.get(
            self.account_data['account_code'],
        )
        self.assertTrue(isinstance(fetched, ManagedAccount))

        # update some account details
        dct = {'username': randomstring(8)}
        self.assertTrue(self.client.accounts.update(fetched, dct))

        # we can get a list of charges.  An empty list shold process.
        charges = fetched.get_charges()
        self.assertEqual(charges, [])

        # charge the account
        charge = fetched.charge(1986, "This charge was created in a unit test yay.")
        self.assertTrue(isinstance(charge, Charge))

        # that charge should appear as pending
        pending = fetched.pending_charges()
        self.assertTrue(charge.id in [c.id for c in pending])
        # note: get_charges only returns 20 charges, but does not return a
        # ResultPage instance due to a bug in the Recurly API; the API
        # returns no paging data.

        # shouldn't be able to register a negative charge.
        self.assertRaises(
            ValueError,
            fetched.charge,
            -200,
            "This should fail.",
        )
        # note: this is not actually handled by Recurly, so if you try to
        # do a raw post for this action Recurly will simply process a
        # negative amount as a positive amount without telling you.

        # invoice the account.
        invoice = fetched.invoice()
        self.assertTrue(isinstance(invoice, Invoice))

        # delete the account
        self.assertTrue(self.client.accounts.delete(fetched))

        # can't delete it again.
        self.assertRaises(RecurlyException,
                          self.client.accounts.delete,
                          fetched)

        # make sure it's gone.
        fetched = self.client.accounts.get(self.account_data['account_code'])
        self.assertTrue(fetched.closed)

if __name__ == '__main__':
    unittest.main()
