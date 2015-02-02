
from    client  import  Client
import  config

def client() :
    """Default client with current offical authenticator, handler."""

    # If new default client type should be used, write new function with funny
    # name to build client, comment out old return statement here, add new one 
    # with date of change.

    return _unsquashable_crumhorn()  # Current as of 2014-08-22.

def _unsquashable_crumhorn() :
    """RSA-based authenticator.  Requests-based handler."""

    from authenticators.rsa_authenticator import  RSAAuthenticator
    from handlers.requests_handler        import  RequestsHandler

    authenticator = RSAAuthenticator( config.USER_ID(), config.CONFIG_PATH() )
    handler       = RequestsHandler( authenticator )
    return Client( handler )
