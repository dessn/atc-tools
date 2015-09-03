#!/usr/bin/env python
import atc_tools
    
# Simple functions that format data into documents suitable to  post to ATC.  
#
# create_incept_post:   Creates document for incepting a target into ATC
# create_lcfit_post:    Creates document for posting a PSNID Supernova 
#                       Light Curve Fit on a transient's ATC page.
#                       Note that this type of post is specific to
#                       the types of parameters being input (PSNID)
# create_host_post:     Creates document for posting an association between
#                       a transient and the galaxy associated with that 
#                       transient (assuming both are already incepted 
#                       targets on the ATC)
#                       Note that the association is one way (points from a 
#                       transient to its host; not vice-versa)  
# send_posts:           Used to send a collection of documents to the ATC.
#                       This includes any of the above listed types of posts.

# NOTE: It is not clear how well posting a very large number of 
#       create_lcfit_post() documents will work.  
#       Is wise to break into chunks of ~10 when inserting those.

###############################################################################

def create_incept_post( target_id, ra, dec, flag = "decimal", 
                        transient = None ) :
    """Take a target_id, R.A., Dec. and whether or not the target is a
    transient and return a document ready to be posted to ATC."""

    doc = dict()

    # A target_id is mandatory for all posts.

    doc[ "target_id" ] = target_id

    # Special attachment marking this post as an incept.  Use of the incept
    # attachment is restricted to administrators and inceptors.  The incept
    # attachment may only be included in a target's first post.  Re-posting 
    # an incept attachment will fail.  The content of the attachment is not
    # important, ATC actually overwrites it with just a timestamp.

    doc[ "incept" ] = dict()

    # Coordinates are useful.
    
    doc[ "coordinates" ] = dict()
    if flag == "sexagesimal" :
        doc[ "coordinates" ][ "__format__" ] = "sexagesimal"
        doc[ "coordinates" ][ "ra"  ] = ra
        doc[ "coordinates" ][ "dec" ] = dec
    else :
        doc[ "coordinates" ][ "ra"  ] = float( ra  )
        doc[ "coordinates" ][ "dec" ] = float( dec )


    if transient is not None :
        doc[ "transient" ] = transient

    return doc

###############################################################################

def create_lcfit_post( target_id, 
                       mjd, phase, flux, flux_error, data_flag, band, 
                       chi2, fit_type, ra, dec,
                       stamps, image,
                       zprior, psnid_run, itype_best, 
                       bayes, fitprob, zfit ) :

    """Create an LCFIT post suitable for posting to ATC."""

    doc = dict()

    # A target_id is mandatory for all posts.

    doc[ "target_id" ] = target_id

    # LCFIT is a dictionary of lists.

    lcfit = dict()
    lcfit[ "mjd"        ] = list()
    lcfit[ "phase"      ] = list()
    lcfit[ "flux"       ] = list()
    lcfit[ "flux_error" ] = list()
    lcfit[ "data_flag"  ] = list()
    lcfit[ "band"       ] = list()
    lcfit[ "chi2"       ] = list()
    lcfit[ "fit_type"   ] = list()
    lcfit[ "image"      ] = list()
    lcfit[ "stamps"     ] = list()
    lcfit[ "ra"         ] = list()
    lcfit[ "dec"        ] = list()

    # Some of these are also lists but they are not the mega lists.
    
    lcfit[ "zprior"     ] = zprior 
    lcfit[ "psnid_run"  ] = psnid_run 
    lcfit[ "itype_best" ] = itype_best 
    lcfit[ "pbayes"     ] = bayes
    lcfit[ "fitprob"    ] = fitprob
    lcfit[ "zfit"       ] = zfit
   
    # LCFIT file has a very particular format.
    # Ensure that the lists are of the correct data type

    for item in mjd:        lcfit[ "mjd"        ].append( float( item ))
    for item in phase:      lcfit[ "phase"      ].append( float( item ))
    for item in flux:       lcfit[ "flux"       ].append( float( item ))
    for item in flux_error: lcfit[ "flux_error" ].append( float( item ))
    for item in data_flag:  lcfit[ "data_flag"  ].append( float( item ))
    for item in band:       lcfit[ "band"       ].append(        item  )
    for item in chi2:       lcfit[ "chi2"       ].append( float( item ))
    for item in fit_type:   lcfit[ "fit_type"   ].append(   int( item ))

    for item in image:      
        if item == "0":     lcfit[ "image"      ].append(        None  )
        else:               lcfit[ "image"      ].append(        item  )
        
    for item in stamps: 
        if item == "0":     lcfit[ "stamps"     ].append(        None  )
        else:               lcfit[ "stamps"     ].append(        item  )

    for item in ra: 
        if item == "0":     lcfit[ "ra"         ].append(        None  )
        else:               lcfit[ "ra"         ].append( float( item ))

    for item in dec:   
        if item == "0":     lcfit[ "dec"        ].append(        None  )
        else:               lcfit[ "dec"        ].append( float( item ))


    # Attach to the document.

    doc[ "lcfit" ] = lcfit
    return doc

###############################################################################

def create_host_post( target_id, host_id ) :
    """Given a target that is hopefully a transient, associate another target
    that is hopefully not a transient with it as a host galaxy."""

    doc = dict()

    # A target_id is mandatory for all posts.

    doc[ "target_id" ] = target_id

    # Build the host galaxy attachment.

    host = dict()
    host[ "target_id" ] = host_id

    # Attach to the document.

    doc[ "host_galaxy" ] = host
    return doc

###############################################################################

def send_posts( doc_or_docs, test_mode = False ) :
    """Send a post.  Note that now incept's go to posts, 
    not targets anymore!"""

    client  = atc_tools.client()
    posts   = client.posts
    return posts.post( doc_or_docs, test_mode = test_mode )

###############################################################################

if __name__ == "__main__" :

    import argparse
    import pprint

    parser = argparse.ArgumentParser( description = "TESTING STUFF" )
    parser.add_argument( "--test", "-t", help = "test mode or not", 
                         action = "store_true" )
    args = parser.parse_args()

