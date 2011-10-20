import functools
from recurly.serialization import parse_xml, parse_errors, ResultsPage

def injectcaller(fn):
    """
    Attaches a "caller" attribute to a response object representing partial
    function.  The "caller" partial is a bound method that retains a
    reference to its owner.
    """
    @functools.wraps(fn)
    def wraps(self, *args, **kwargs):
        response = fn(self, *args, **kwargs)
        if isinstance(response, ResultsPage):
            response.caller = functools.partial(fn, self)
        return response
    return wraps

def autoparse(fn):
    """
    Wraps python-requests calls to Recurly.  Causes requests to raise
    standard errors when appropriate.  Results are parsed before being
    returned.
    """
    @injectcaller
    @functools.wraps(fn)
    def wraps(self, *args, **kwargs):
        response = fn(self, *args, **kwargs)
        if not response:
            raise parse_errors(response)
        if not response.content or response.content.isspace():
            return True
        if hasattr(self, '_client'):
            return parse_xml(response, self._client)
        return parse_xml(response)
    return wraps
