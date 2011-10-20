import functools
import string

def trace(fn):
    """
    this can be used to decorate python-requests calls in order to trace the
    requests and responses being made.  It can be handy during development
    """
    @functools.wraps(fn)
    def wraps(self, url, *args, **kwargs):
        print "%s %s" % (string.upper(fn.func_name), url)
        for a in args:
            print "arg: %r" % a
        for k, v in kwargs.items():
            print "%r: %r" % (k, v)
        return fn(self, url, *args, **kwargs)
    return wraps
