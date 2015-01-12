#!/usr/bin/env python

import  argparse
import  pprint

import  atc_tools

#

parser = argparse.ArgumentParser( description = "Apply or remove a simple tag to a target or list of targets." )
parser.add_argument( "action"    ,       help = "Tag action [%(choices)s]"                     , choices = [ "apply", "remove" ]   )
parser.add_argument( "tag"       ,       help = "Name of tag to apply or remove."                                                  )
parser.add_argument( "target_ids",       help = "List of targets to act upon."                 , nargs = "+"                       )
parser.add_argument( "--test"    , "-t", help = "Test mode: Server only validates, no inserts.", action = "store_true"             )
parser.add_argument( "--comment" , "-c", help = "Comment text if any."                         , default = argparse.SUPPRESS       ) 
args = parser.parse_args()

#

status = args.action == "apply"

#

docs = list()
for target_id in args.target_ids :
    doc = dict()
    doc[ "target_id" ] = target_id
    doc[ args.tag    ] = status
    if "comment" in args :
        doc[ "text" ] = args.comment
    docs.append( doc )

pprint.pprint( docs )

# 

client   = atc_tools.default_client()
service  = client.service( "posts" )
response = service.post( docs, test_mode = args.test )
pprint.pprint( response )
