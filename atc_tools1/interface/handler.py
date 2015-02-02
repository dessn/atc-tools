
class Handler ( object ) :
    """Assembles, signs (using an `Authenticator`), and sends messages to
    ATC applications and services.  Interprets responses from ATC as JSON
    objects or translates errors into `ATCException` objects of appropriate
    type."""

    def __init__( self, authenticator ) :
        self.authenticator = authenticator

    def __call__( self, path, method = "GET", data = None, params = None, test_mode = False ) :
        """Assemble, sign, and send a request."""

        return self._handle_request( path, method, data, params, test_mode )

    def _handle_request( self, path, method, data, params, test_mode ) :
        """Concrete subclasses provide an implementation.

        Headers sent must include
            Content-Type:       application/json (if request JSON data is being sent)
            ATC-User-ID:        (provided by authenticator)
            ATC-Request-Time:   (Unix time in milliseconds)
            ATC-Signature:      (provided by authenticator, depends on final request URL.
        Headers can also optionally include
            ATC-Test_Mode:      (with a dummy value).
        
        Optional headers may have no effect for some methods."""

        raise NotImplementedError
