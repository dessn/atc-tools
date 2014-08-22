
import errno
import os
import re

def create_directory( dirname, permissions = None ) :
    """Like mkdir -p."""
    try :
        os.makedirs( dirname )
    except OSError as e :
        if e.errno == errno.EEXIST and os.path.isdir( dirname ) :
            pass
        else :
            raise
    if permissions is not None :
        os.chmod( dirname, permissions )

def uncamelize( name ) :
    """Convert name from CamelCase to underscore-separated."""
    new_name = re.sub( "(.)([A-Z][a-z]+)", r"\1_\2", name )
    return re.sub( "([a-z0-9])([A-Z])", r"\1_\2", new_name ).lower()
