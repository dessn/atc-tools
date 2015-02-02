
import utils

class Client ( object ) :

    def __init__( self, handler ) :
        self.handler   = handler
        self._services = dict()

    @property
    def service_names( self ) :
        return sorted( self._services.keys() )

    def register_service( self, service_type, name = None ) :
        if name is None :
            name = utils.uncamelize( service_type.__name__ )
        self._services[ name ] = service_type( self.handler )

    def unregister_service( self, name ) :
        del self._services[ name ]

    def service( self, name ) :
        try :
            return self._services[ name ]
        except KeyError :
            raise AttributeError( "no service registered as '%s'" % name )

    def __getattr__( self, name ) :
        return self.service( name )

#       try :
#           return self._services[ name ]
#       except KeyError :
#           raise AttributeError( "no service registered as '%s'" % name )
