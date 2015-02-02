
import  sys
import  time

import  config
import  exceptions
import  utilities

def create( name, handler ) :
    """Service factory."""

    typename = utilities.camelize( name )
    service  = globals().setdefault( typename, type( typename, ( Service, ), {} ) )
    return service( handler )

class Service ( object ) :
    """Base Service class."""

    def __init__( self, handler ) :
        self.handler = handler

    @utilities.lazy
    def service_name( self ) :
        return utilities.uncamelize( self.__class__.__name__ )

    @utilities.lazy
    def service_root( self ) :
        return "/%s/" % self.service_name

    @utilities.lazy
    def service_url( self ) :
        return config.ATC_REST_URL() + self.service_root

    # The following are generic method stubs that need not be implemented by
    # every service subclass, but prescribe a uniform interface for similar
    # tasks over all services.  

    def get( self, _id, include = None, exclude = None ) :
        """Retrieve one document matching document identifier."""

        params = {}
        if include is not None :
            params[ "include" ] = include
        if exclude is not None :
            params[ "exclude" ] = exclude
        self._process_request( "GET", _id, params = params )

    def list( self, skip = None, limit = None, order = None, include = None, exclude = None, count = False, params = {} ) :
        """Attempt to retrieve a block of multiple documents."""

        if skip is not None :
            params[ "skip" ] = skip
        if limit is not None :
            params[ "limit" ] = limit
        if order is not None :
            params[ "order" ] = order
        if include is not None :
            params[ "include" ] = include
        if exclude is not None :
            params[ "exclude" ] = exclude
        if count :
            params[ "count" ] = 1
        return self._process_request( "GET", params = params )

    def post( self, doc, test_mode = False ) :
        """Attempt to create a new document."""

        self._process_request( "POST", data = doc, test_mode = test_mode )

    def put( self, _id, doc ) :
        """Attempt to replace or update a document with a matching document
        identifier."""

        return self._process_request( "PUT", _id, doc )

    def delete( self, _id ) :
        """Attempt to delete a document with a matching document identifier."""

        return self._process_request( "DELETE", _id )

    def _process_request( self, method, path = "", data = None, params = None, test_mode = False ) :
        """Prepare, manage, and post-process calls to the ATC REST API.

        Headers sent must include
            Content-Type:       application/json (if request JSON data is being sent)
            ATC-Request-Time:   (Unix time in milliseconds)
            ATC-User-ID:        (provided by authenticator)
            ATC-Signature:      (provided by authenticator, depends on final request URL)
        Headers can also optionally include
            ATC-Test-Mode:      (with a dummy value).
        
        Optional headers may have no effect for some methods."""

        # ATC-specific headers excluding user ID and signature.

        headers = dict()
        if data :
            headers[ "Content-Type" ] = "application/json"
        if test_mode :
            headers[ "ATC-Test-Mode" ] = 1
        headers[ "ATC-Request-Time" ] = int( time.time() * 1.0e6 )

        # The handler signs and executes the request.

        response_data, status_code = self.handler( self.service_url, method, headers, data, params )

        # Intercept server and ATC application or service errors and translate
        # them into an appropriate `ATCException` if necessary.  If internal
        # server error is raised, suggest loudly that ATC may be offline.

        try :
            if response_data is not None and "__error__" in response_data :
                error_data = response_data[ "__error__" ]
                error_type = exceptions.from_typename( error_data[ "type" ] )
                raise error_type( error_data[ "args" ] )
            if status_code is not None and status_code >= 400 :
                raise exceptions.from_status_code( status_code )
        except exceptions.InternalServerError :
            sys.stderr.write( "\n\033[1m\033[4m**********        SORRY TRY AGAIN LATER?        **********\033[0m\n" )
            sys.stderr.write( "\033[1m\033[4m**********     ATC MAY BE OFFLINE RIGHT NOW     **********\033[0m\n" )
            sys.stderr.write( "\033[1m\033[4m**********      GURU MEDITATION ERROR: 500      **********\033[0m\n\n" )
            raise

        # Return the response data.

        return response_data

class Fields ( Service ) :

    def post( self, doc, test_mode = False ) :
        if doc[ "__units__" ] == "degrees" :
            doc[ "ra"  ] = float( doc[ "ra"  ] )
            doc[ "dec" ] = float( doc[ "dec" ] )
        return super( Fields, self ).post( doc, test_mode )

