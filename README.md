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

Important.  If your login name on the machine where you run atc-tools stuff 
from is different from your NERSC username, then you need to set (assuming
bash):

    export ATC_USER_ID=nersc_id

Where `nersc_id` is your NERSC username.  To make this permanent stick it in
your shell resource login file (.bashrc).
