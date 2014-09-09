
import json
import time

import requests

from .. import config
from .. import exceptions
from .. import interface

class RequestsHandler ( interface.Handler ) :
    """Implements a requests-based handler."""

    def __init__( self, authenticator ) :
        self.authenticator = authenticator

    def _handle_request( self, path, method, data, params, test_mode ) :

        # Use the "prepared request" approach, because we need the exact
        # URL that requests is going to use to send the message for the 
        # construction and eventual verification of the digital signature.
        # (http://docs.python-requests.org/en/latest/user/advanced/#prepared-requests)

        session = requests.Session()
        if data :
            raw_request = requests.Request( method, config.ATC_REST_URL() + path, data = json.dumps( data ), params = params )
        else :
            raw_request = requests.Request( method, config.ATC_REST_URL() + path, params = params )
        request = session.prepare_request( raw_request )

        # Append ATC-specific headers including the signature as computed
        # by some authenticator.

        if data :
            request.headers[ "Content-Type" ] = "application/json"
        request.headers[ "ATC-User-ID"      ] = self.authenticator.user_id
        request.headers[ "ATC-Request-Time" ] = int( time.time() * 1.0e6 )
        request.headers[ "ATC-Signature"    ] = self.authenticator( request.headers[ "ATC-Request-Time" ], method, request.url, data )
        if test_mode :
            request.headers[ "ATC-Test-Mode" ] = 1

        # Send request and receive response.  Then intercept any errors and
        # translate them into an appropriate ATCException object if necessary.
        # Otherwise just return the JSON response (if there is one).

        response = session.send( request )
#       print dir( response.request.body )
#       print response.request.body
        try :
            data = response.json()
        except ValueError :
            data = None
        return exceptions.check_for_errors( data, response.status_code )
