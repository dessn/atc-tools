
from .. import utils

class Service ( object ) :
    """Represents an ATC service endpoint.  Core REST API methods may be 
    implemented but not accessible (depending on user role).  Extensions
    provided on a subclass-by-subclass basis may also be available."""

    def __init__( self, handler ) :
        self.handler = handler

    @property
    def name( self ) :
        """ATC service name."""

        try :
            return self._name
        except AttributeError :
            self._name = utils.uncamelize( self.__class__.__name__ )
            return self._name

    @property
    def path( self ) :
        """ATC service path."""

        try :
            return self._path
        except AttributeError :
            self._path = "/%s/" % self.name
            return self._path

    # The following are purely generic method stubs that need not be 
    # implemented by every service subclass, but prescribe a uniform
    # interface for similar tasks over all services.

    def post( self, doc, test_mode = False ) :
        """Attempt to create a new document."""
        return self.handler( self.path, "POST", doc, test_mode = test_mode )

    def get( self, _id, include = None, exclude = None ) :
        """Retrieve one document matching document identifier."""

        params = {}
        if include is not None :
            params[ "include" ] = include
        if exclude is not None :
            params[ "exclude" ] = exclude
        return self.handler( self.path + _id, params = params )

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
        return self.handler( self.path, params = params )

    def put( self, _id, doc ) :
        """Attempt to replace or update a document with a matching document
        identifier."""

        return self.handler( self.path + _id, "PUT", doc )

    def delete( self, _id ) :
        """Attempt to delete a document with a matching document identifier."""
        return self.handler( self.path + _id, "DELETE" )
