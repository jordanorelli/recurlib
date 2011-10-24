from recurly import xmldict

class BaseModel(object):
    known_attributes = ()
    pk_attrib = 'id'

    def _filter_dict(self, dct):
        """Filters a dictionary, removing all items in the dictionary whose
        keys are not listed in known_attributes."""
        return dict((k, v) for k, v in dct.items()
                    if k in self.__class__.known_attributes)

    def __init__(self, *args, **kwargs):
        dct = self._filter_dict(kwargs)
        for k, v in dct.items():
            setattr(self, k, v)
        if 'client' in kwargs:
            self._client = kwargs['client']

    def to_xml(self):
        from recurly.serialization import xmldict
        dct = self._filter_dict(self.__dict__)
        return xmldict(self.__class__.item_tag, dct)

    @property
    def pk(self):
        if hasattr(self.__class__, 'pk_attrib'):
            return getattr(self, self.__class__.pk_attrib)
        else:
            return self.id
