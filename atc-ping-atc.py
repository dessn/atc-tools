#!/usr/bin/env python

"""Ping ATC, retrieve, and optionally list recent pings."""

import  argparse
import  pprint

import  atc_tools

# Parse command line.

parser = argparse.ArgumentParser( description = __doc__, formatter_class = argparse.RawTextHelpFormatter )
parser.add_argument( "--quiet", "-q", help = "Ping only, skip listing the recent pings.", action = "store_true" )

parser.epilog = """
ATC hosts a ping service in its REST API.  This service can be used to guess
whether the ATC application is running normally, or appears to be offline.  A
ping request also returns a list of recently active users, with a few minutes
of accuracy.  Note there may be significant clock skew in ping timestamps, on
the order of several seconds.

The original reason for the ping service is to circumvent a Shibboleth-imposed
inactivity timeout that was far too short for most ATC web application users.
ATC web pages served to clients contain a JavaScript transponder routine that
simply checks in with ATC about every 10 minutes or so.  This keeps users from
having to re-authenticate too often (every half-hour or hour or so).  RCT did
this because he had no control over how Shibboleth was configured at NERSC.
"""

args = parser.parse_args()

# Query for pings and print them if requested.

doc = atc_tools.client().pings.list()
if not args.quiet :
    pprint.pprint( doc )
