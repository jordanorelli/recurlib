from xml.etree import cElementTree
from xml.etree.cElementTree import Element

class BaseModel(object):
    known_attributes = ()

    def __init__(self, *args, **kwargs):
        for attrib in self.__class__.known_attributes:
            setattr(self, attrib, kwargs.get(attrib, None))
        self._client = kwargs.get('client', None)
        if hasattr(self, 'managed_class') and self._client:
            self.__class__ = self.managed_class

    def to_xml(self):
        elem = Element(self.__class__.item_tag)
        for k,v in self.__dict__.items():
            if k not in self.__class__.known_attributes:
                continue
            if not v:
                continue
            child = Element(k)
            child.text = str(v)
            elem.append(child)
        return cElementTree.tostring(elem)
