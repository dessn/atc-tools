#!/usr/bin/env python

import  argparse
import  pprint

import  atc_tools

# Command line.

parser = argparse.ArgumentParser( description = "Register an ATEL with possibly more than one target." )
parser.add_argument( "atel"         ,       help = "Number of the ATEL mentioning the targets."   , type = int                  )
parser.add_argument( "target_ids"   ,       help = "List of targets."                             , nargs = "+"                 )
parser.add_argument( "--test"       , "-t", help = "Test mode: Server only validates, no inserts.", action = "store_true"       )
parser.add_argument( "--comment"    , "-c", help = "Comment text if any."                         , default = argparse.SUPPRESS ) 
args = parser.parse_args()

# Docs.

docs = list()

for target_id in args.target_ids :
    doc = dict()
    doc[ "target_id" ] = target_id
    doc[ "atel"      ] = dict( number = args.atel )
    if "comment" in args :
        doc[ "text" ] = args.comment
    docs.append( doc )

pprint.pprint( docs )

# Post it.

client   = atc_tools.default_client()
service  = client.service( "posts" )
response = service.post( docs, test_mode = args.test )
pprint.pprint( response )
