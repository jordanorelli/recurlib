class RecurlyException(Exception):
    """ Recurly base exception. """
    pass

class RecurlyValidationException(RecurlyException):
    """ Raise when encountering errors in validation. """
    pass

class RecurlyConnectionException(RecurlyException):
    """ Raised when unable to connect to the Recurly parent server. """
    pass

class RecurlyNotFoundException(RecurlyException):
    pass

class RecurlyServerException(RecurlyException):
    pass

class RecurlyServiceUnavailbleException(RecurlyException):
    pass
