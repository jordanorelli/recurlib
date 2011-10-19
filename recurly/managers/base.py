from recurly.managers.decorators import autoparse

class BaseManager(object):
    endpoint = ''

    def __init__(self, client):
        self._client = client

    @autoparse
    def create(self, obj):
        return self._client.post(self.endpoint, data=obj.to_xml())
