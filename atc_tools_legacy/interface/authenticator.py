
class Authenticator ( object ) :
    """Constructs digital signatures for authenticating atc-tools users 
    to ATC applications and services."""

    def __init__( self, user_id ) :
        self.user_id = user_id

    def __call__( self, request_time, method, url, data ) :
        """Construct and return a signature."""
        payload  = "%s\n" % self.user_id
        payload += "%d\n" % request_time
        payload += "%s\n" % method
        payload += "%s\n" % url
        if data :
            if type( data ) is dict :
                payload += "\n".join( sorted( data.keys() ) )
            elif type( data ) is list :
                keys = set()
                for entry in data :
                    keys.update( entry.keys() )
                payload += "\n".join( sorted( list( keys ) ) )
        return self._create_signature( payload )

    def _create_signature( self, payload ) :
        """Concrete subclasses provide an implementation."""
        raise NotImplementedError

