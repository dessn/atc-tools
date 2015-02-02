
import base64
import os

import rsa

from .. import config
from .. import interface
from .. import utils

def RSA_KEYPAIR_SIZE() :
    """Default size for generated RSA developer keys."""
    return 512

def RSA_SIGNATURE_HASH() :
    """Default signature hashing method."""
    return "SHA-256"

def RSA_KEYPAIR_PREFIX() :
    """Default prefix for ATC developer keypair filenames.  This is set to
    "atc-dev."  Users may set the `ATC_KEYPAIR_PREFIX` environment variable to
    override."""
    return os.environ.get( "ATC_KEYPAIR_PREFIX", "atc-dev" )

def PRIVATE_RSA_KEYFILE_PATH() :
    """Default path to the ATC developer private keyfile.  Constructed from
    `CONFIG_PATH()` and `RSA_KEYPAIR_PREFIX.` See those functions for overrides
    using environment variables."""
    return os.path.join( config.CONFIG_PATH(), "%s-private.pem" % RSA_KEYPAIR_PREFIX() )

def rsa_keypair_filenames( prefix ) :
    """Return RSA keypair filenames based on a prefix."""

    public_key_filename  = "%s-public.pem"  % prefix
    private_key_filename = "%s-private.pem" % prefix
    return public_key_filename, private_key_filename

def rsa_keypair_paths( config_path, prefix ) :
    """Return possible RSA keypair paths."""

    public_key_filename, private_key_filename = rsa_keypair_filenames( prefix )
    public_key_path  = os.path.join( ".", public_key_filename )
    private_key_path = os.path.join( config_path, private_key_filename )
    return public_key_path, private_key_path

def valid_rsa_keypair_paths( config_path, prefix, force ) :
    """Return valid RSA keypair paths.  Throw a ValueError if either or both of
    the public or private keyfiles already exist.  If `force` is true then any
    existing keyfiles are ignored and can be overwritten."""

    public_key_path, private_key_path = rsa_keypair_paths( config_path, prefix )
    if not force and ( os.path.isfile( public_key_path ) or os.path.isfile( private_key_path ) ) :
        raise ValueError( "public or private keyfile already exists" )
    return public_key_path, private_key_path

def create_rsa_keypair( config_path = config.CONFIG_PATH(), prefix = RSA_KEYPAIR_PREFIX(), keysize = RSA_KEYPAIR_SIZE(), force = False ) :
    """Create a new ATC developer API keypair.  The public key is written to a
    world-readable file deposited in the current working directory.  This is to
    be uploaded to ATC via a user's profile page.  The private key is written
    to a user-readable file that is deposited to the API config path.  If the 
    API config path does not exist, it is created."""

    public_key_path, private_key_path = valid_rsa_keypair_paths( config_path, prefix, force )
    utils.create_directory( config_path, 0700 )
    public_key, private_key = rsa.newkeys( keysize )
    with open( public_key_path, "w" ) as stream :
        stream.write( public_key.save_pkcs1() )
    os.chmod( public_key_path, 0644 )
    with open( private_key_path, "w" ) as stream :
        stream.write( private_key.save_pkcs1() )
    os.chmod( private_key_path, 0600 )
    return public_key_path, private_key_path

class RSAAuthenticator ( interface.Authenticator ) :

    """Implements an RSA-based authenticator."""

    @classmethod
    def create( cls, user_id = None, private_keyfile_path = None ) :
        """Create authenticator.  Use defaults if no arguments are provided."""
        user_id              = user_id              or config.USER_ID()
        private_keyfile_path = private_keyfile_path or PRIVATE_RSA_KEYFILE_PATH()
        with open( private_keyfile_path, "r" ) as stream :
            private_key = rsa.PrivateKey.load_pkcs1( stream.read() )
        return cls( user_id, private_key )

    def __init__( self, user_id, private_key ) :
        super( RSAAuthenticator, self ).__init__( user_id )
        self.private_key = private_key

    def _create_signature( self, payload ) :
        return base64.b64encode( rsa.sign( payload, self.private_key, RSA_SIGNATURE_HASH() ) )
