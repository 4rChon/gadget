import importlib
import pkgutil
import traceback

class AuthenticationError(Exception):
    """Rasied by require_auth when the user is not authenticated."""
    
    pass

class WaitingForAuthenticationNotice(Exception):
    """Raised by require_auth when waiting for authentication verification to complete."""
    
    pass

class UnsupportedProtocol(Exception):
    """Raised anywhere in a protocol module to indicate that the protocol cannot be used."""
    
    pass

class UnsupportedPlugin(Exception):
    """Raised anywhere in a plugin module to indicate that the plugin cannot be used."""
    
    pass

def find_modules_in_package(path):
    """Scan a Python package for modules."""
    
    try:
        package = importlib.import_module(path)
    except Exception as e:
        print "Exception raised when scanning package %s:" % (path,)
        
        traceback.print_exc()
    
    return find_modules_in_directory(os.path.dirname(package.__file__))

def find_modules_in_directory(path):
    """Scan a directory for Python modules."""
    
    for _, name, isPkg in pkgutil.iter_modules([path]):
        if not isPkg:
            yield name
