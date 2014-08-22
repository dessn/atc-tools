#!/usr/bin/env python

import argparse

import atc_tools.authenticators
import atc_tools.config

# Command line.

parser = argparse.ArgumentParser( description = "Generate ATC developer keypair (RSA style)." )
parser.add_argument( "--force", "-f", help = "Forced overwrite of any existing keyfiles.", action = "store_true" )
args = parser.parse_args()

# We are currently using an RSA keypair system.

public_key_path, private_key_path = atc_tools.authenticators.create_rsa_keypair( force = args.force )

# Friendly message that tells our users what to do now...

print
print "".join( [ "=" for i in range( 80 ) ] )
print
print "Public ATC developer keyfile:" 
print
print "   ", public_key_path
print
print "Upload the public ATC developer keyfile found at the path listed above to"
print "your ATC user profile page, which is located here:"
print
print "   ", "/".join( [ atc_tools.config.ATC_WEB_URL(), "profile" ] )
print
print "Once your public ATC developer keyfile is uploaded and the administrator"
print "has granted you the developer role, you can start using atc-tools."
print
print "Just FYI, the private ATC developer keyfile is located at:"
print
print "   ", private_key_path
print
print "But leave your private ATC developer keyfile alone!"
print
print "".join( [ "=" for i in range( 80 ) ] )
print
