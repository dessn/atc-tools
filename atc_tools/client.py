
import  services

class Client ( object ) :
    """Service factory."""

    def __init__( self, handler ) :
        self._handler  = handler
        self._services = dict()

    def __getattr__( self, name ) :
        """Return service."""

        try :
            return self._services[ name ]
        except KeyError :
            self._services[ name ] = services.create( name, self._handler )
            return self._services[ name ]
