
import  sys

class ATCException ( Exception ) :
    """Errors thrown by ATC applications, services are translated on client
    side into hierarchy with `ATCException` at root."""

    pass

class Module ( object ) :

    def from_typename( self, typename ) :
        """Dynamically build, return `ATCException` type given a typename.  If
        typename given is "ATCException" then `ATCException` type is returned. No
        guarantee that a created type is real or legal in any sense..."""
    
        return ATCException if typename == "ATCException" else globals().setdefault( typename, type( str( typename ), ( ATCException, ), {} ) )
    
    def from_status_code( self, status_code ) :
        """Dynamically build, return `ATCException` type given HTTP error status
        code.  If status code is unrecognized, error type like `UnknownErrorNNN` is
        returned, where NNN is the unknown status code.  If status code passed is
        unrecognized, throw `ValueError`."""
    
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
   
        return self.from_typename( typename )

    def __getattr__( self, name ) :
        return self.from_typename( name )

_ref, sys.modules[ __name__ ] = sys.modules[ __name__ ], Module()
