from xml.etree import cElementTree
from recurly.managers.decorators import autoparse

class BaseManager(object):
    endpoint = ''

    def __init__(self, client):
        self._client = client

    @autoparse
    def get(self, pk):
        return self._client.get("%s/%s" % (self.endpoint, pk))

    @autoparse
    def create(self, obj):
        return self._client.post(self.endpoint, data=obj.to_xml())

    @autoparse
    def delete(self, obj):
        if type(obj) is str:
            return self._client.delete("%s/%s" % (self.endpoint, obj))
        return self._client.delete("%s/%s" % (self.endpoint, obj.pk))

    @autoparse
    def update(self, obj, dct):
        elem = cElementTree.Element(obj.__class__.item_tag)
        for k, v in dct.items():
            child = cElementTree.Element(k)
            child.text = str(v)
            elem.append(child)
        xml = cElementTree.tostring(elem)
        return self._client.put("%s/%s" % (self.endpoint, obj.pk), data=xml)
