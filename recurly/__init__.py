from xml.etree import cElementTree

def xmldict(tag_name, dct):
    elem = cElementTree.Element(tag_name)
    for k, v in dct.items():
        child = cElementTree.Element(k)
        child.text = str(v)
        elem.append(child)
    return cElementTree.tostring(elem)
