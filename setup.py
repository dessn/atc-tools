
from    distutils.core  import  setup
import  os

# Scripts to install on all systems.

scripts = [ 
        "atc"                   ,
        "atc-create-user"       ,
        "atc-delete-post"       ,
        "atc-generate-keypair"  ,
        "atc-ping-atc"          ,
        "atc-register-atel"     ,
        "atc-tag-aat"           ,
        "atc-tag-simple"        ,
        "atc-targets-for-aat"   ,
        "atc-untag-aat"
        ]

# Additional scripts for NERSC installations.

if "NERSC_HOST" in os.environ :
    scripts += [ "atc-post-aat-spectra" ]

# Path to scripts.

scripts = [ "scripts/%s" % script for script in scripts ]

# Package and sub-packages.

packages = [ "atc_tools", "atc_tools.authenticators", "atc_tools.handlers", "atc_tools.ext" ]

# Package setup.  The requirements may be too stringent and older versions
# may be alright.  Haven't checked.

setup(  name            =   "atc-tools"                                     ,
        version         =   "1.0.0"                                         ,
        description     =   "Python ATC client reference implementation."   ,
        author          =   "R. C. Thomas"                                  ,
        author_email    =   "rcthomas@lbl.gov"                              ,
        url             =   "https://github.com/dessn/atc-tools"            ,
        requires        =   [ "rsa (>=3.1.4)", "requests (>=2.4.1)" ]       ,
        packages        =   packages                                        ,
        scripts         =   scripts                                         )

