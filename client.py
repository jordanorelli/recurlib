from recurly import verification
from recurly.decorators import bubble, trace
from recurly.exceptions import *
from recurly.managers import AccountManager, ChargeManager
from requests import session
from requests.models import AuthObject
from xml.etree.cElementTree import Element

class Client():
    """ A Recurly REST API client. """

    def __init__(self, subdomain, api_key, private_key):
        """
        Creates a REST client for interacting with the Recurly servers.  API
        credentials can be found by logging in at Recurly.com and visiting
        https://yourdomain.recurly.com/developer/api_access (mutatis mutandis)
        """
        self.url = 'https://%s.recurly.com' % subdomain
        self.private_key = private_key
        self._session = session(
            auth = AuthObject(api_key, ''),
            headers = {
                'Accept': 'application/xml',
                'Content-Type': 'application/xml; charset=utf-8',
                'User-Agent': "Jordan Orelli's Python Client",
            })
        self.accounts = AccountManager(self)
        self.charges = ChargeManager(self)

    @trace
    @bubble
    def get(self, url, *args, **kwargs):
        """
        This is a proxy HTTP GET method on a requests.session object.
        Supplied URL should be a relative URL (e.g. /accounts, not
        api.recurly.com/accounts).  Returns a raw response object.
        """
        return self._session.get(self.url + url, *args, **kwargs)

    @trace
    @bubble
    def post(self, url, *args, **kwargs):
        """
        This is a proxy HTTP POST method on a requests.session object.
        Supplied URL should be a relative URL (e.g. /accounts, not
        api.recurly.com/accounts).  Returns a raw response object.
        """
        return self._session.post(self.url + url, *args, **kwargs)

    @trace
    @bubble
    def put(self, url, *args, **kwargs):
        """
        This is a proxy HTTP PUT method on a requests.session object.
        Supplied URL should be a relative URL (e.g. /accounts, not
        api.recurly.com/accounts).  Returns a raw response object.
        """
        return self._session.put(self.url + url, *args, **kwargs)

    @trace
    @bubble
    def delete(self, url, *args, **kwargs):
        """
        This is a proxy HTTP DELETE method on a requests.session object.
        Supplied URL should be a relative URL (e.g. /accounts, not
        api.recurly.com/accounts).  Returns a raw response object.
        """
        return self._session.delete(self.url + url, *args, **kwargs)

    def generate_signature(self, claim, args, timestamp=None):
        return verification.generate_signature(claim, args, self.private_key)

    def verify_params(self, claim, args):
        return verification.verify_params(claim, args, self.private_key)
