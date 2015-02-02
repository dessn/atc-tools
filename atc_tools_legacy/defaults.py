
from . import authenticators
from . import client
from . import handlers
from . import services

def default_client() :

    """Authenticator is based on the `RSA` python package, initialized with
    client-wide default settings for user ID and private developer keyfile
    values.  Handler is based on the `requests` python package."""

    auth    = authenticators.RSAAuthenticator.create()
    handler = handlers.RequestsHandler( auth )
    new_client  = client.Client( handler )
    new_client.register_service( services.Comments          )
    new_client.register_service( services.Fields            )
    new_client.register_service( services.Lcfits            )
    new_client.register_service( services.Observatories     )
    new_client.register_service( services.Posts             )
    new_client.register_service( services.Targets           )
    new_client.register_service( services.Users             )
    return new_client
