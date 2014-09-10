#!/usr/bin/env python

import  datetime
import  sys
import  time

import  atc_tools

# Lazy property decorator, can't get enough of it.

def lazy( func ) :
    attr_name = "__" + func.__name__
    @property
    def _lazy( obj ) :
        try :
            return getattr( obj, attr_name )
        except AttributeError :
            setattr( obj, attr_name, func( obj ) )
            return getattr( obj, attr_name )
    return _lazy

# Let's make a class of a target list.

class TargetList ( object ) :

    def __init__( self, limit = 500, sleep_secs = 2 ) :
        self.tag        = "supernova"
        self.limit      = limit
        self.sleep_secs = sleep_secs

    def __repr__( self ) :
        return self.text

    @lazy
    def text( self ) :
        return "%s\n%s" % ( self.header, self.body )

    @lazy
    def header( self ) :
        lines = list()
        lines.append( "#TIMESTAMP %sZ"   % self.timestamp.isoformat( " " )   )
        lines.append( "#TAG %s"          % self.tag                          )
        lines.append( "#CONTACT %s"      % self.contact                      )
        return "\n".join( lines )

    @lazy
    def body( self ) :
        lines = list()
        for doc in self.targets :
            target_id       = doc[ "_id" ]
            ra_degrees      = doc[ "value" ][ "coordinates"   ][ "ra"  ][ "degrees" ]
            dec_degrees     = doc[ "value" ][ "coordinates"   ][ "dec" ][ "degrees" ]
            tag_r_magnitude = doc[ "value" ][ "aat_supernova" ][ "r_magnitude" ]
            tag_r_magnitude = tag_r_magnitude if type( tag_r_magnitude ) is float else float( tag_r_magnitude )
            tag_type        = doc[ "value" ][ "aat_supernova" ][ "type" ]
            lines.append( "%s,%.6f,%.6f,%.2f,%s" % ( target_id, ra_degrees, dec_degrees, tag_r_magnitude, tag_type ) )
        return "\n".join( lines ) + "\n"

    @lazy
    def timestamp( self ) :
        return datetime.datetime.utcnow()

    @lazy
    def contact( self ) :
        print >> sys.stderr, "fetching user's ATC contact information"
        time.sleep( self.sleep_secs )
        doc = self.users_service.get( atc_tools.config.USER_ID(), include = "email" )
        return doc[ "email" ]

    @lazy
    def targets( self ) :

        docs    = list()
        skip    = 0
        include = [ "value.coordinates.ra.degrees", "value.coordinates.dec.degrees", "value.aat_supernova.r_magnitude", "value.aat_supernova.type" ]

        print >> sys.stderr, "fetching tagged targets ... "
        while True :
            print >> sys.stderr, " ... skip = %-5d, limit = %-5d" % ( skip, self.limit )
            time.sleep( self.sleep_secs )
            data  = self.targets_service.list( skip, self.limit, include = include, params = { "tag" : "aat_supernova" } )
            chunk = data[ "docs" ]
            if not chunk :
                break
            docs += chunk
            skip += self.limit
        print >> sys.stderr, " ... fetched %d targets" % len( docs )
        return docs

    @lazy
    def client( self ) :
        return atc_tools.default_client()

    @lazy
    def targets_service( self ) :
        return self.client.service( "targets" )

    @lazy
    def users_service( self ) :
        return self.client.service( "users" )

    @lazy
    def output_filename( self ) :
        return "%s.%sZ.dat" % ( self.tag, self.timestamp.isoformat().translate( None, "-:" ) )

if __name__ == "__main__" :

    import argparse

    parser = argparse.ArgumentParser( description = "Create a SN WG target file for AAT to follow-up." )
    args = parser.parse_args()

    target_list = TargetList()
    with open( target_list.output_filename, "w" ) as stream :
        stream.write( "%s" % target_list )
