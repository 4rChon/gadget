import os
import importlib
import pkgutil
import traceback
import imp

from gadget.globals import Globals

class AuthenticationError(Exception):
    """Rasied by require_auth when the user is not authenticated."""
    
    pass

class WaitingForAuthenticationNotice(Exception):
    """Raised by require_auth when waiting for authentication verification to complete."""
    
    pass

class UnsupportedException(Exception):
    """Base class for UnsupportedProtocol/UnsupportedPlugin."""
    
    pass

class UnsupportedProtocol(UnsupportedException):
    """Raised anywhere in a protocol module to indicate that the protocol cannot be used."""
    
    pass

class UnsupportedPlugin(UnsupportedException):
    """Raised anywhere in a plugin module to indicate that the plugin cannot be used."""
    
    pass

def get_modules_in_package(path):
    """Scan a Python package for modules, importing and yielding each one."""
    
    try:
        package = importlib.import_module(path)
    except Exception as e:
        print "Exception raised when scanning package %s:" % (path,)
        
        traceback.print_exc()
    
    return get_modules_in_directory(os.path.dirname(package.__file__))

def get_modules_in_directory(path):
    """Scan a directory for Python modules, importing and yielding each one."""
    
    for _, name, isPkg in pkgutil.iter_modules([path]):
        if not isPkg:
            try:
                yield imp.load_source(name, "%s/%s.py" % (path, name))
            except UnsupportedException as e:
                print "Module %s is unsupported. (%s)" % (name, e.message)
            except Exception as e:
                print "Exception raised when importing module %s:" % (name,)
                
                traceback.print_exc()

def get_setting(key, default=None):
    """Retrieve a setting from gadget_settings.py, or a default if it doesn't exist."""
    
    try:
        return getattr(Globals.settings, key)
    except:
        if default == Exception:
            raise
        else:
            return default
