#!/usr/bin/env python

import  argparse
import  datetime
import  os
import  pprint
import  sys
import  tarfile

from    astropy.io  import  fits
import  scipy

import  atc_tools
import  atc_tools.exceptions

# Command line.

parser = argparse.ArgumentParser( description = "Extract and post spectra to ATC from an archive file (at NERSC ONLY)." )
parser.add_argument( "archive_path" , help = "path to archive file"  )
parser.add_argument( "--test", "-t" , help = "Test mode: Server only validates, no inserts.", action = "store_true" )
args = parser.parse_args()

# Archive name required to be in atc-uploads/multi-target/aat.  Note that this
# script should be run at NERSC, won't work right from elsewhere.

if os.path.dirname( args.archive_path ) != "/project/projectdirs/dessn/www/atc-uploads/multi-target/aat" :
    raise ValueError( "invalid archive path: %s" % args.archive_path )

# Determine which archive members are interesting for extraction based
# on what the filename looks like.

members = list()

with tarfile.open( args.archive_path, "r:gz" ) as archive :

    for i, member in enumerate( archive ) :
    
        # Progress meter newline.
    
        if i % 80 == 0 :
            sys.stderr.write( "\n" )
    
        # Keep if it looks right.
    
        tokens = member.name.split( "/" )
    
        try :
            top, status, version, field, filename = tokens
            tokens = filename.split( "_" )
            if status == "reduced" and tokens[ 0 ] == field and tokens[ 2 ] == version and filename.endswith( ".fits" ) :
                members.append( member )
                sys.stderr.write( "*" )
            else :
                sys.stderr.write( "." )
        except ValueError :
            sys.stderr.write( "." )
        except IndexError :
            sys.stderr.write( "." )

    sys.stderr.write( "\n\n" )

    # List and extract selected files from archive.  Make the order of
    # extraction be like (assumed) worst to best.
    
    members.sort( key = lambda member : member.name.count( "+" ) )
    members.sort( key = lambda member : member.name.split( "/" )[ 2 ] )
    for member in members :
        print member.name

    archive.extractall( os.environ[ "GSCRATCH" ], members = members )

# Iterate over extracted archive members to build posts.

count = 0
docs  = list()
tags  = dict()
ras   = list()
decs  = list()

for member in members :

    # Open FITS file.

    file_name = "%s/%s" % ( os.environ[ "GSCRATCH" ], member.name )
    hdulist = fits.open( file_name )

    # Wavelength axis.

    crval1 = hdulist[ 0 ].header[ "CRVAL1" ]
    cdelt1 = hdulist[ 0 ].header[ "CDELT1" ]
    crpix1 = hdulist[ 0 ].header[ "CRPIX1" ]
    naxis1 = hdulist[ 0 ].header[ "NAXIS1" ]
    wl = crval1 + cdelt1 * ( scipy.arange( naxis1 ) - crpix1 + 1 )

    # UTC date.

    utdate = hdulist[ 0 ].header[ "UTDATE" ]
    utdate = utdate.replace( ":", "-" )

    # Test-parse the date.

    test_date = datetime.datetime.strptime( utdate, "%Y-%m-%d" )

    # Iterate over records to build posts.

    for i, record in enumerate( hdulist[ "FIBRES" ].data ) :

        count += 1

        # Extract record type and name.
        
        record_type    = record[ "TYPE" ]
        record_name    = record[ "NAME" ]
        record_comment = record[ "COMMENT" ]

        # Just in case target has not been incepted.

        record_ra  = scipy.rad2deg( record[ "RA"  ] )
        record_dec = scipy.rad2deg( record[ "DEC" ] )

        # Skip non-program fibers.

        if record_type != "P" :
#           print "skipped non-program fibre (%s/%s) " % ( record_type, record_name )
            continue

        # Skip fibers not of interest.

        tag = record_comment.split()[ 0 ]
        tags.setdefault( tag, 0 )
        tags[ tag ] += 1

        if tag not in [ "FStar", "SN_host", "SN_host_faint", "StrongLens", "Transient", "WhiteDwarf" ] :
#           print "skipped %s" % record_comment
            continue

        # Output something of interest.

        print "%s %s %s %s %s" % ( file_name, utdate, record_type, record_name, record_comment )

        # Extract flux and flux error.
            
        flux  = hdulist[ 0 ].data[ i ]
        error = hdulist[ 1 ].data[ i ]

        # Create a mask for good entries (flux and error both non-nan, variance positive).

        good = ( ~scipy.isnan( flux ) ) & ( ~scipy.isnan( error ) ) & ( error >= 0.0 ) # last causes warning.

        # If the number of good entries is not big enough, complain.

        num_bad_entries = scipy.sum( ~good )
        pct_bad_entries = float( num_bad_entries ) / len( flux ) * 100.0
        if pct_bad_entries > 2.0 :
            warning = "Warning! Many bad entries (NaN flux/variance or negative variance --- %.2f%% > 2%%)." % pct_bad_entries
            print warning
            record_comment += " " + warning + " "
#           raise ValueError( "too many bad entries (%.2f%% > 2%%) for %s" % ( pct_bad_entries, record_name ) )

        # Scrub the spectrum of the bad entries and convert variance to error.

        flux  = flux[ good ]
        error = scipy.sqrt( error[ good ] )

        # Build spectrum attachment.

        spectrum = dict( wl = wl[ good ].tolist(), flux = flux.tolist(), error = error.tolist(), nersc_path = args.archive_path, utc_date = utdate, observatory_id = "AAT" ) 

        # Build post and append to list.

        doc = dict( target_id = record_name, spectrum = spectrum, text = "From archive file %s (fiber %d).  %s" % ( member.name, i, record_comment ) )

        docs.append( doc )
        
        # In case this target has not been incepted.

        ras.append( record_ra )
        decs.append( record_dec )

    # Close FITS file.

    hdulist.close()

# Summarize for user.

for tag in tags :
    print "%-40s %d" % ( tag, tags[ tag ] )
print len( docs ), "/", count, "of interest"

# Set up the REST client.

client      = atc_tools.default_client()
posts_svc   = client.service( "posts" )
targets_svc = client.service( "targets" )

# See which targets do not exist.

for i, doc in enumerate( docs ) :
    target_id = doc[ "target_id" ]
    try :
        response = targets_svc.get( target_id )
    except atc_tools.exceptions.NotFound :
        print "Target not found: %s" % target_id

        doc[ "incept" ] = dict()
        doc[ "coordinates" ] = dict()
        doc[ "coordinates" ][ "ra"  ] =  ras[ i ]
        doc[ "coordinates" ][ "dec" ] = decs[ i ]

client   = atc_tools.default_client()
service  = client.service( "posts" )
response = service.post( docs, test_mode = args.test )
pprint.pprint( response ) 
