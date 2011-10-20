import functools
import string

def trace(fn):
    @functools.wraps(fn)
    def wraps(self, url, *args, **kwargs):
        print "%s %s" % (string.upper(fn.func_name), url)
        for a in args:
            print "arg: %r" % a
        for k, v in kwargs.items():
            print "%r: %r" % (k, v)
        return fn(self, url, *args, **kwargs)
    return wraps

def bubble(fn):
    """
    Wraps python-requests calls to cause them to raise errors as they occur.
    """
    @functools.wraps(fn)
    def wraps(self, url, *args, **kwargs):
        response = fn(self, url, *args, **kwargs)
        if not response:
            raise response.error
        return response
    return wraps
