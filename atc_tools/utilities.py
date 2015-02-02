
import  errno
import  os
import  re

def create_directory( dirname, permissions = None ) :
    """Like Unix 'mkdir -p' command."""

    try :
        os.makedirs( dirname )
    except OSError as e :
        if e.errno == errno.EEXIST and os.path.isdir( dirname ) :
            pass
        else :
            raise
    if permissions is not None :
        os.chmod( dirname, permissions )

def camelize( name ) :
    """Convert name from underscore-separated to CamelCase."""

    return "".join( word.capitalize() or "_" for word in name.split( "_" ) )

def uncamelize( name ) :
    """Convert name from CamelCase to underscore-separated."""

    new_name = re.sub( "(.)([A-Z][a-z]+)", r"\1_\2", name )
    return re.sub( "([a-z0-9])([A-Z])", r"\1_\2", new_name ).lower()

def lazy( func ) :
    """Decorator to allow lazy initialization."""

    attr = func.__name__
    if attr.startswith( "_" ) :
        attr = "_private" + attr # avoid collisions
    else :
        attr = "_" + attr

    @property
    def _lazy( obj ) :
        try :
            return getattr( obj, attr )
        except AttributeError :
            setattr( obj, attr, func( obj ) )
            return getattr( obj, attr )

    return _lazy
