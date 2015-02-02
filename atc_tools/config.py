
import  os

def ATC_ROOT_URL() :
    """Root URL for ATC applications and services."""

    return "https://portal-auth.nersc.gov/atc2"

def ATC_WEB_URL() :
    """Root URL for ATC web application."""

    return ATC_ROOT_URL() + "/web"

def ATC_REST_URL() :
    """Root URL for ATC REST application interface."""

    return ATC_ROOT_URL() + "/rest"

def USER_ID() :
    """Unique string identifying atc-tools user to ATC applications, services.
    By default, local machine login or user name.  To override, `ATC_USER_ID`
    environment variable is set."""

    return os.environ.get( "ATC_USER_ID", os.environ[ "LOGNAME" ] )

def CONFIG_PATH() :
    """Directory path containing user-specific application data like 
    private developer keyfiles, application resource files, cached 
    data, etc.  By default, `$HOME/.atc-config`.  Use `ATC_CONFIG_PATH`
    environment variable to override."""

    return os.environ.get( "ATC_CONFIG_PATH", os.path.join( os.environ[ "HOME" ], ".atc-config" ) )
