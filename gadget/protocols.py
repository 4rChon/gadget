import os
import traceback
from itertools import chain

from gadget import get_modules_in_package, get_modules_in_directory, get_setting, UnsupportedProtocol
from gadget.globals import Globals

class IProtocol(object):
    """Expected interface for a protocol, in addition to build_protocol in the module.
       You aren't required to subclass this, only to implement all of its methods and members.
       None of this applies if you are writing a protocol for some other purpose, such as the Echoer or manhole."""
    
    PROTOCOL_NAME = None #display name for the protocol, used in global messages and whatnot
    
    def send_message(self, context):
        """Called by gadget.messages.send_message to inform the protocol of incoming messages."""
        
        raise NotImplementedError
    
    def is_authed(self, context):
        """Called by gadget.plugins.is_authed to determine whether a user is authorized to run a priviledged command."""
        
        raise NotImplementedError

def load_protocols():
    """Load all protocols."""
    
    modules = chain()
    
    for iterable in ([get_modules_in_package("gadget.default_protocols")] +
                     [get_modules_in_directory(dir) for dir in get_setting("PROTOCOL_PATHS")]):
        modules = chain(modules, iterable)
    
    for module in modules:
        if hasattr(module, "build_protocol"):
            print "Loading protocol", module.__name__
            
            try:
                protocol = module.build_protocol()
                
                if protocol:
                    Globals.protocols.update({module.__name__: protocol})
            except UnsupportedProtocol as e:
                print "Protocol %s is unsupported: %s" % (module.__name__, e.message)
        else:
            print "Warning: protocol %s does not have a build_protocol function" % (module.__name__,)

def have_required_settings(*args):
    """Checks gadget_settings.py for required settings."""
    
    try:
        for key in args:
            get_setting(key, Exception)
        
        return True
    except:
        return False

def parse_hostname(string):
    """Parse a string of the format hostname:port."""
    
    try:
        split = string.split(":")
        split[1] = int(split[1])
        
        assert 0 <= split[1] <= 65535
        return split
    except IndexError:
        print "Error in settings:\n'%s' is not a valid hostname:port combination." % (string,)
        
        raise
    except ValueError:
        print "Error in settings:\n%r is not a number." % (split[1],)
        
        raise
    except AssertionError:
        print "Error in settings:\n%d is not a valid port. (try somewhere in 0-65535)" % (split[1],)
        
        raise
