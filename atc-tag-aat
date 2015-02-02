#!/usr/bin/env python

"""Apply an aat_supernova tag to a target or list of targets."""

import  argparse
import  pprint

import  atc_tools

parser = argparse.ArgumentParser( description = __doc__ )
parser.add_argument( "csv_file"     , help = "CSV file containing target and tag contents."                         )
parser.add_argument( "--quiet", "-q", help = "Output warnings and errors only."             , action = "store_true" )
parser.add_argument( "--test" , "-t", help = "Test mode: Server only validates, no inserts.", action = "store_true" )
args = parser.parse_args()

docs = list()
with open( args.csv_file, "r" ) as stream :

    # Not using the csv module because I don't quite get it...

    for line in stream :
        tokens = line.strip().split( "," )
        if not tokens :
            continue
        if tokens[ 0 ].startswith( "#" ) :
            continue
        if len( tokens ) < 5 :
            raise ValueError( "not enough fields:\n%s" % line )

        # Build document. Removal condition goes last in case it's got commas
        # in it.  Probably not 100% fool-proof.  Note that types matter.
        
        doc = dict()
        doc[ "target_id"     ] = tokens[ 0 ]

        doc[ "aat_supernova" ] = dict()
        doc[ "aat_supernova" ][ "r_magnitude"       ] = float( tokens[ 1 ] )
        doc[ "aat_supernova" ][ "type"              ] =        tokens[ 2 ]
        doc[ "aat_supernova" ][ "priority"          ] = int  ( tokens[ 3 ] )
        doc[ "aat_supernova" ][ "removal_condition" ] = ",".join( tokens[ 4 : ] ).strip()

        docs.append( doc )

# Post documents, optionally display response.

doc = atc_tools.client().posts.post( docs, test_mode = args.test )
if not args.quiet :
    pprint.pprint( doc )
