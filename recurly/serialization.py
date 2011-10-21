from dateutil.parser import parse as parse_date
from inspect import getmembers, isclass
from recurly import models
from recurly.exceptions import exception_class_map, RecurlyException
from warnings import warn
from xml.etree import cElementTree

_known_types = {
    'boolean': bool,
    'integer': int,
    'datetime': parse_date,
}

_item_tags = {}
_collection_tags = {}

model_classes = getmembers(models, isclass)
for label, cls in model_classes:
    if hasattr(cls, 'item_tag'):
        _item_tags[cls.item_tag] = cls
    if hasattr(cls, 'collection_tag'):
        _collection_tags[cls.collection_tag] = cls

def parse_item(elem, client=None):
    item = _item_tags[elem.tag](client=client)

    for child in list(elem):
        if 'type' in child.attrib:
            if child.attrib['type'] in _known_types:
                val = _known_types[child.attrib['type']](child.text)
            else:
                warn("Unkown type '%s' specified in xml tag '%s'"
                     % (child.attrib['type'], elem.tag))
                val = child.text
        else:
            val = child.text

        if not hasattr(item, child.tag):
            warn("Setting unknown attribute '%s' to '%r' on instance of '%s'"
                 % (child.tag, val, item.__class__.__name__))

        setattr(item, child.tag, val)
    return item

def parse_errors(response):
    """
    Parses error info from raw response objects.  The error itself isn't
    raised, it is just constructed.
    """
    try:
        cls = exception_class_map.get(response.status_code, RecurlyException)
        errortexts = []
        if response.content and not response.content.isspace():
            elem = cElementTree.fromstring(response.content)
            if elem.tag != 'errors':
                raise RecurlyException("Expected xml root tag of <errors>, \
                                       received unkown tag '%s'" % elem.tag)
            for child in list(elem):
                if child.tag != 'error':
                    raise RecurlyException("Expected xml child tag of \
                                           <error>, received unkown tag \
                                           '%s'" % child.tag)
                errortexts.append(child.text)
        return cls('.'.join(errortexts) or cls.__doc__)

    except Exception as omfg:
    # I pray that this block never executes.
        e = RecurlyException("Error parsing Recurly error xml.  Ugh.", omfg)
    e.args += (response,)
    return e

def parse_collection(elem, client=None):
    items = []
    cls = _collection_tags[elem.tag]

    page_tags = set(('current_page', 'per_page', 'total_entries'))
    elem_tags = set([child.tag for child in list(elem)])
    if page_tags <= elem_tags:
        return ResultsPage(elem, client)

    for child in list(elem):
        if child.tag != cls.item_tag:
            warn("Skipped unknown tag %s" % child.tag)
            continue
        items.append(parse_element(child, client))
    return items

def parse_element(elem, client=None):
    if 'type' in elem.attrib:
        if elem.attrib['type'] in ['array', 'collection']:
            return parse_collection(elem, client)
    return parse_item(elem, client)

def parse_xml(response, client=None):
    elem = cElementTree.fromstring(response.content)
    if elem.tag == 'errors':
        raise parse_errors(response)
    return parse_element(elem, client)

class ResultsPage(object):
    def __init__(self, elem, client=None):
        current_page_elem = elem.find('current_page')
        per_page_elem = elem.find('per_page')
        total_entries_elem = elem.find('total_entries')
        elem.remove(current_page_elem)
        elem.remove(per_page_elem)
        elem.remove(total_entries_elem)

        self.current_page = int(current_page_elem.text)
        self.per_page = int(per_page_elem.text)
        self.total_entries = int(total_entries_elem.text)
        self.items = [parse_element(child, client) for child in list(elem)]

    def __iter__(self):
        return self.items.__iter__()

    def __getitem__(self, key):
        return self.items.__getitem__(key)

    def __len__(self):
        return self.items.__len__()

    def next_page(self):
        page = self.caller(page=self.current_page+1)
        page.caller = self.caller
        return page
