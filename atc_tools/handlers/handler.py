
class Handler ( object ) :
    """Handles ATC REST API calls."""

    def __init__( self, authenticator ) :
        self.authenticator = authenticator

    def __call__( self, url, method, headers, data, params ) :
        return self._handle_request( url, method, headers, data, params )

    def _handle_request( self, url, method, headers, data, params ) :
        """Subclass implementation."""

        raise NotImplementedError
