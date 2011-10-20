class RecurlyException(Exception):
    """ Recurly base exception. """
    pass

class RecurlyBadRequestException(RecurlyException):
    """
    The request was invalid or could not be understood by the server.
    Resubmitting the request will likely result in the same error.
    (http status 400)
    """
    pass

class RecurlyUnauthorizedException(RecurlyException):
    """
    The username and password credentials are missing or invalid for the
    given request. (http status 401)
    """
    pass

class RecurlyAccountDeliquentException(RecurlyException):
    """
    Your Recurly account is in production mode but is not in good standing.
    Please pay any outstanding invoices. (http status 402)
    """
    pass

class RecurlyForbiddenException(RecurlyException):
    """
    The login is attempting to perform an action it does not have privileges
    to access. The login credentials are correct. (http status 403)
    """
    pass

class RecurlyNotFoundException(RecurlyException):
    """
    The resource was not found. This may be returned if the given account
    code or subscription plan does not exist. The response body will explain
    which resource was not found. (http status 404)
    """
    pass

class RecurlyPreconditionFailedException(RecurlyException):
    """
    The request was unsuccessful because a condition was not met. For example,
    this message may be returned if you attempt to cancel a subscription for
    an account that has no subscription. (http status 412)
    """
    pass

class RecurlyUnprocessableEntityException(RecurlyException):
    """
    Could not process a POST or PUT request because the request is invalid.
    See the response body for more details. (http status 422)
    """
    pass

class RecurlyInternalServerErrorException(RecurlyException):
    """
    The server encountered an error while processing your request and failed.
    (http status 500)
    """
    pass

class RecurlyGatewayErrorException(RecurlyException):
    """
    The load balancer or web server has trouble connecting to the Recurly app.
    Please try the request again. (http status 502)
    """
    pass

class RecurlyUnavailableException(RecurlyException):
    """
    The service is temporarily unavailable. Please try the request again.
    (http status 503)
    """
    pass

class RecurlyValidationException(RecurlyException):
    """ Raise when encountering errors in validation. """
    pass

def get_exception(response):
    """
    Takes a python-requests response object and casts it to the appropraite
    RecurlyException object.
    """
    exception_class = {
        400: RecurlyBadRequestException,
        401: RecurlyUnauthorizedException,
        402: RecurlyAccountDeliquentException,
        403: RecurlyForbiddenException,
        404: RecurlyNotFoundException,
        412: RecurlyPreconditionFailedException,
        422: RecurlyUnprocessableEntityException,
        500: RecurlyInternalServerErrorException,
        502: RecurlyGatewayErrorException,
        503: RecurlyUnavailableException,
    }.get(response.status_code, RecurlyException)
