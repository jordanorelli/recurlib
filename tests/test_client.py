#!/usr/bin/env python
from recurly.client import Client
from credentials import credentials as creds

if __name__ == '__main__':
    c = Client(creds['subdomain'], creds['api_key'], creds['private_key'])
