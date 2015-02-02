#!/usr/bin/env python

"""Associate one or more targets with a given Astronomer's Telegram in ATC."""

import  argparse
import  pprint

import  atc_tools

# Parse command line.

parser = argparse.ArgumentParser( description = __doc__ )
parser.add_argument( "atel"      ,       help = "Number of the ATEL mentioning the targets."   , type = int                  )
parser.add_argument( "target_ids",       help = "List of targets."                             , nargs = "+"                 )
parser.add_argument( "--comment" , "-c", help = "Comment text if any."                         , default = argparse.SUPPRESS ) 
parser.add_argument( "--quiet"   , "-q", help = "Output warnings and errors only."             , action = "store_true"       )
parser.add_argument( "--test"    , "-t", help = "Test mode: Server only validates, no inserts.", action = "store_true"       )
args = parser.parse_args()

# Create documents to post.

docs = list()

for target_id in args.target_ids :
    doc = dict()
    doc[ "target_id" ] = target_id
    doc[ "atel"      ] = dict( number = args.atel )
    if "comment" in args :
        doc[ "text" ] = args.comment
    docs.append( doc )

pprint.pprint( docs )

# Post documents.

doc = atc_tools.client().posts.post( docs, test_mode = args.test )
if not args.quiet :
    pprint.pprint( doc )
