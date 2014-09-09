#!/usr/bin/env python

import  argparse
import  pprint

import  atc_tools

parser = argparse.ArgumentParser( description = "Apply an aat_supernova tag to a target or list of targets." )
parser.add_argument( "csv_file"     , help = "CSV file containing targets and tag contents." )
parser.add_argument( "--test", "-t" , help = "Test mode: Server only validates, no inserts.", action = "store_true" )
args = parser.parse_args()

docs = list()
with open( args.csv_file, "r" ) as stream :

    # I don't understand the csv module personally...

    for line in stream :

        tokens = line.strip().split( "," )
        if not tokens :
            continue
        if tokens[ 0 ].startswith( "#" ) :
            continue
        if len( tokens ) < 5 :
            raise ValueError( "Not enough fields:\n%s" % line )

        # Build document. Removal condition goes last in case it's got commas in it.
        # My solution is probably not 100% fool-proof.  Note that types matter.
        
        doc = dict()
        doc[ "target_id"     ] = tokens[ 0 ]

        doc[ "aat_supernova" ] = dict()
        doc[ "aat_supernova" ][ "r_magnitude"       ] = float( tokens[ 1 ] )
        doc[ "aat_supernova" ][ "type"              ] =        tokens[ 2 ]
        doc[ "aat_supernova" ][ "priority"          ] = int  ( tokens[ 3 ] )
        doc[ "aat_supernova" ][ "removal_condition" ] = ",".join( tokens[ 4 : ] ).strip()

        docs.append( doc )

# Now let's awesome...

client   = atc_tools.default_client()
service  = client.service( "posts" )
response = service.post( docs, test_mode = args.test )
pprint.pprint( response ) 
