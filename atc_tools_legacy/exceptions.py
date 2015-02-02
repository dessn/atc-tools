
from interface import ATCException

def _type_from_typename( typename ) :

    """Dynamically build and return an `ATCException` type given a typename.
    If the typename given is "ATCException" then the `ATCException` type is
    returned.  WARNING: It is not guaranteed that a type created with this
    function is real or legal in any sense."""

    if typename == "ATCException" :
        return ATCException
    else :
        module = globals()
        module[ typename ] = type( str( typename ), ( ATCException, ), {} )
        return module[ typename ]

def _type_from_status_code( status_code ) :

    """Dynamically build and return an `ATCException` type given an HTTP
    error status code.  If the status code is unrecognized, an error type
    like `UnknownErrorNNN` is returned, where NNN is the unknown status
    code.  If the status code passed is unrecognized and doesn't look 
    like an actual HTTP error status code, a `ValueError` is thrown."""

    http_error_status_codes = {
        400 : "BadRequest"                  , 401 : "Unauthorized"                  , 402 : "PaymentRequired"               ,
        403 : "Forbidden"                   , 404 : "NotFound"                      , 405 : "MethodNotAllowed"              ,
        406 : "NotAcceptable"               , 407 : "ProxyAuthenticationRequired"   , 408 : "RequestTimeout"                ,
        409 : "Conflict"                    , 410 : "Gone"                          , 411 : "LengthRequired"                ,
        412 : "PreconditionFailed"          , 413 : "RequestEntityTooLarge"         , 414 : "RequestURITooLong"             ,
        415 : "UnsupportedMediaType"        , 416 : "RequestedRangeNotSatisfiable"  , 417 : "ExpectationFailed"             ,
        418 : "Teapot"                      , 422 : "UnprocessableEntity"           , 423 : "Locked"                        ,
        424 : "FailedDependency"            , 426 : "UpgradeRequired"               , 428 : "PreconditionRequired"          ,
        429 : "TooManyRequests"             , 431 : "RequestHeaderFieldsTooLarge"   , 500 : "InternalServerError"           ,
        501 : "NotImplemented"              , 502 : "BadGateway"                    , 503 : "ServiceUnavailable"            ,
        504 : "GatewayTimeout"              , 505 : "HTTPVersionNotSupported"       , 506 : "VariantAlsoNegotiates"         ,
        507 : "InsufficientStorage"         , 508 : "LoopDetected"                  , 509 : "BandwidthLimitExceeded"        ,
        510 : "NotExtended"                 , 511 : "NetworkAuthenticationRequired" , 598 : "NetworkReadTimeoutError"       ,
        599 : "NetworkConnectTimeoutError"  }

    try :
        typename = http_error_status_codes[ status_code ]
    except KeyError :
        if status_code >= 400 :
            typename = "UnknownError%d" % status_code
        else :
            raise ValueError( "illegal error status code" )

    return _type_from_typename( typename )

def check_for_errors( data, status_code ) :

    """Intercept server and ATC application or service errors and
    translate them into an appropriate `ATCException` if necessary.
    Otherwise just return the data."""

    if data is not None and "__error__" in data :
        error_data = data[ "__error__" ]
        error_type = _type_from_typename( error_data[ "type" ] )
        raise error_type( error_data[ "args" ] )

    if status_code is not None and status_code >= 400 :
        error_type = _type_from_status_code( status_code )
        raise error_type

    return data
