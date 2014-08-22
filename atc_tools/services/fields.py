
from .. import interface

class Fields ( interface.Service ) :

    def post( self, doc ) :
        if doc[ "__units__" ] == "degrees" :
            doc[ "ra"  ] = float( doc[ "ra"  ] )
            doc[ "dec" ] = float( doc[ "dec" ] )
        return super( Fields, self ).post( doc )
