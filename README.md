atc-tools
=========

Client-side scripting for ATC in Python 2.7.

Prerequisites
-------------

You will need the python RSA module and the Requests module.  To install them I
recommend pip:

    pip install rsa
    pip install requests

That should do it.

Setting Up
----------

Once prerequisites are squared away, you need to upload a public developer key
to ATC to use the interface.  This is used to sign and verify signatures on all
accesses to ATC.  To do this, you do:

    atc-generate-keypair.py

This will drop a public key file in the current working directory, and stash
away a private key (by default) at $HOME/.atc-config.  Follow the instructions
that the script outputs.  You will be directed to upload the public keyfile 
(NOT THE PRIVATE ONE) to ATC at your ATC profile page.
