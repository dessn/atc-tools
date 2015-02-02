
import  json

import  requests

from    handler import  Handler

class RequestsHandler ( Handler ) :

    def _handle_request( self, url, method, headers, data, params ) :
        
        # Use the "prepared request" approach, because we need the exact URL
        # that requests is going to use to send the message for the
        # construction and eventual verification of the digital signature.
        # (http://docs.python-requests.org/en/latest/user/advanced/#prepared-requests)

        session = requests.Session()
        if data :
            raw_request = requests.Request( method, url, data = json.dumps( data ), params = params )
        else :
            raw_request = requests.Request( method, url, params = params )
        request = session.prepare_request( raw_request )

        # Append headers including user ID and signature from authenticator.

        for key, value in headers.iteritems() :
            request.headers[ key ] = value

        request.headers[ "ATC-User-ID"   ] = self.authenticator.user_id
        request.headers[ "ATC-Signature" ] = self.authenticator( request.headers[ "ATC-Request-Time" ], method, request.url, data )

        # Send request and receive JSON response.
        
        response = session.send( request )
        try :
            response_data = response.json()
        except ValueError :
            response_data = None

        # Return response data and response status code.

        return response_data, response.status_code
