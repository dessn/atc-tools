
import  base64
import  os

import  rsa

from    ..              import  utilities
from    authenticator   import  Authenticator

class RSAAuthenticator ( Authenticator ) :
    """RSA-based authenticator."""

    def __init__( self, user_id, config_dir ) :
        super( RSAAuthenticator, self ).__init__( user_id )
        self.config_dir = config_dir

    def _create_signature( self, payload ) :
        """Create RSA-based signature from payload."""

        return base64.b64encode( rsa.sign( payload, self.private_key, self.signature_hash ) )

    def create_keypair( self, force = False ) :
        """Create new ATC developer API keypair. Public key goes into a file
        deposited in current working directory.  This is then uploaded to ATC
        at user's profile page.  Private key is written to a user-readable file
        in API config directory, created if it does not yet exist."""

        # Ensure public key does not exist yet (unless force).

        public_key_path = os.path.join( os.getcwd(), self.public_key_filename )
        if not force and os.path.isfile( public_key_path ) :
            raise ValueError( "public keyfile already exists: %s" % public_key_path )

        # Ensure private key does not exist yet (unless force).

        if not force and os.path.isfile( self.private_key_path ) :
            raise ValueError( "private keyfile already exists: %s" % self.private_key_path )

        # Create keypair.

        public_key, private_key = rsa.newkeys( self.keypair_size )

        # Write world-readable public key.

        with open( public_key_path, "w" ) as stream :
            stream.write( public_key.save_pkcs1() )
        os.chmod( public_key_path, 0644 )

        # Write user-readable public key in API config path.

        utilities.create_directory( self.config_dir, 0700 )
        with open( self.private_key_path, "w" ) as stream :
            stream.write( private_key.save_pkcs1() )
        os.chmod( self.private_key_path, 0600 )

        # Return keyfile paths.

        return public_key_path, self.private_key_path

    @utilities.lazy
    def private_key( self ) :
        """RSA private key object."""

        with open( self.private_key_path, "r" ) as stream :
            return rsa.PrivateKey.load_pkcs1( stream.read() )

    @utilities.lazy
    def keypair_size( self ) :
        """Default size for generated RSA developer keys."""

        return 512

    @utilities.lazy
    def signature_hash( self ) :
        """Default signature hashing method."""

        return "SHA-256"

    @utilities.lazy
    def keypair_prefix( self ) :
        """Default prefix for ATC developer keypair filenames.  Users may set
        `ATC_KEYPAIR_PREFIX` environment variable to override."""

        return os.environ.get( "ATC_KEYPAIR_PREFIX", "atc-dev" )

    @utilities.lazy
    def public_key_filename( self ) :
        """RSA public key filename based on prefix."""
    
        return "%s-public.pem" % self.keypair_prefix

    @utilities.lazy
    def private_key_filename( self ) :
        """RSA private key filename based on prefix."""

        return "%s-private.pem" % self.keypair_prefix

    @utilities.lazy
    def private_key_path( self ) :
        """Default path to ATC developer private keyfile."""

        return os.path.join( self.config_dir, self.private_key_filename )
