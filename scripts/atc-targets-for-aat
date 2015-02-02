#!/usr/bin/env python

"""Create a DES-SN WG target file for AAT to follow-up."""

import  argparse
import  datetime
import  sys
import  time

import  atc_tools
import  atc_tools.config
import  atc_tools.utilities

class TargetList ( object ) :

    def __init__( self, limit = 500, sleep_secs = 2, quiet = False ) :
        self.tag        = "supernova"
        self.limit      = limit
        self.sleep_secs = sleep_secs
        self.quiet      = quiet
        self.client     = atc_tools.client()

    def __repr__( self ) :
        return self.text

    @atc_tools.utilities.lazy
    def text( self ) :
        return "%s\n%s" % ( self.header, self.body )

    @atc_tools.utilities.lazy
    def header( self ) :
        lines = list()
        lines.append( "#TIMESTAMP %sZ"   % self.timestamp.isoformat( " " )   )
        lines.append( "#TAG %s"          % self.tag                          )
        lines.append( "#CONTACT %s"      % self.contact                      )
        return "\n".join( lines )

    @atc_tools.utilities.lazy
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

    @atc_tools.utilities.lazy
    def timestamp( self ) :
        return datetime.datetime.utcnow()

    @atc_tools.utilities.lazy
    def contact( self ) :
        self.message( "fetching user's ATC contact information" )
        time.sleep( self.sleep_secs )
        doc = self.client.users.get( atc_tools.config.USER_ID(), include = "email" )
        return doc[ "email" ]

    @atc_tools.utilities.lazy
    def targets( self ) :

        docs    = list()
        skip    = 0
        include = [ "value.coordinates.ra.degrees", "value.coordinates.dec.degrees", "value.aat_supernova.r_magnitude", "value.aat_supernova.type" ]

        self.message( "fetching tagged targets ... " )
        while True :
            self.message( " ... skip = %-5d, limit = %-5d" % ( skip, self.limit ) )
            time.sleep( self.sleep_secs )
            data  = self.client.targets.list( skip, self.limit, include = include, params = { "tag" : "aat_supernova" } )
            chunk = data[ "docs" ]
            if not chunk :
                break
            docs += chunk
            skip += self.limit
        self.message( " ... fetched %d targets" % len( docs ) )
        return docs

    @atc_tools.utilities.lazy
    def output_filename( self ) :
        return "%s.%sZ.dat" % ( self.tag, self.timestamp.isoformat().translate( None, "-:" ) )

    def message( self, text ) :
        if self.quiet :
            return
        print text

# Parse command line.

parser = argparse.ArgumentParser( description = __doc__ )
parser.add_argument( "--quiet", "-q", help = "Output warnings and errors only.", action = "store_true" )
args = parser.parse_args()

# Create and dump target list.

target_list = TargetList( quiet = args.quiet )
with open( target_list.output_filename, "w" ) as stream :
    stream.write( "%s" % target_list )
