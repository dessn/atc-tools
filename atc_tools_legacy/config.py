
"""Package configuration settings."""

import os

def ATC_ROOT_URL() :
    """Root URL for all ATC applications and services."""
    return "https://portal-auth.nersc.gov/atc2"

def ATC_WEB_URL() :
    """Root URL for the ATC web application."""
    return ATC_ROOT_URL() + "/web"

def ATC_REST_URL() :
    """Root URL for the ATC REST application interface."""
    return ATC_ROOT_URL() + "/rest"

def USER_ID() :
    """Unique string identifying an atc-tools user to ATC applications
    and services.  By default this is set to the user's current local
    machine login or user name.  Use the `ATC_USER_ID` environment 
    variable to override."""
    return os.environ.get( "ATC_USER_ID", os.environ[ "LOGNAME" ] )

def CONFIG_PATH() :
    """Directory path containing user-specific application data like 
    private developer keyfiles, application resource files, cached 
    data, etc.  This is set to `$HOME/.atc-config` by default.  Use
    the `ATC_CONFIG_PATH` environment variable to override."""
    return os.environ.get( "ATC_CONFIG_PATH", os.path.join( os.environ[ "HOME" ], ".atc-config" ) )
