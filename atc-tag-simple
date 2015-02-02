#!/usr/bin/env python

"""Apply or remove a simple tag on a target or list of targets."""

import  argparse
import  pprint

import  atc_tools

# Parse command line.

parser = argparse.ArgumentParser( description = __doc__, formatter_class = argparse.RawTextHelpFormatter )
parser.epilog = """
applying a tag to several targets:

    atc-tag-simple.py apply qso DES14C3ppk DES14C3asz DES14C3cux 
        DES14C3cwz -c "Long non-periodic variability."

removing a tag from a target:

    atc-tag-simple.py remove qso DES14C3ppk -c "Oops, non-QSO."

"""
parser.add_argument( "action"    ,       help = "Tag action."                                  , choices = [ "apply", "remove" ]   )
parser.add_argument( "tag"       ,       help = "Name of tag to apply or remove."                                                  )
parser.add_argument( "target_ids",       help = "List of targets IDs to act upon."             , nargs = "+"                       )
parser.add_argument( "--comment" , "-c", help = "Comment text if any."                         , default = argparse.SUPPRESS       ) 
parser.add_argument( "--quiet"   , "-q", help = "Output warnings and errors only."             , action = "store_true"             )
parser.add_argument( "--test"    , "-t", help = "Test mode: Server only validates, no inserts.", action = "store_true"             )
args = parser.parse_args()

# Compute boolean tag status (true or false).

status = args.action == "apply"

# Prepare document(s).

docs = list()
for target_id in args.target_ids :
    doc = dict()
    doc[ "target_id" ] = target_id
    doc[ args.tag    ] = status
    if "comment" in args :
        doc[ "text" ] = args.comment
    docs.append( doc )

# Optionally show documents to user.

if not args.quiet :
    pprint.pprint( docs )

# Post documents, optionally display response.

doc = atc_tools.client().posts.post( docs, test_mode = args.test )
if not args.quiet :
    pprint.pprint( doc )
