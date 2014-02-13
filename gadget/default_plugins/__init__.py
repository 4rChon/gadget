import random
from functools import wraps

from twisted.internet.defer import Deferred

from gadget import AuthenticationError, WaitingForAuthenticationNotice
from gadget.globals import Globals

def get_auth_failure_msg():
    return random.choice(Globals.settings.AUTH_FAILURE_MESSAGES)

def is_authed(environ):
    try:
        return environ["protocol"].is_authed(environ)
    except KeyError:
        print "Warning: is_authed called without protocol in environ dictionary"
        
        return False

def require_auth(func):
    """Decorator for checking authentication before running a command."""
    
    @wraps(func)
    def wrapper(self, cmd, args, environ):
        authed = is_authed(environ)
        
        def complete(result):
            if not result:
                return make_deferred(get_auth_failure_msg())
            else:
                return func(self, cmd, args, environ)
        
        if   type(authed) is bool:
            return complete(authed)
        elif authed.__class__ is Deferred: #type(Deferred()) returns <type 'instance'> (Deferred is an old-style class)
            authed.addCallback(complete) #default callback chaining behaviour returns the usual result from the command handler after verifying authentication
            
            raise WaitingForAuthenticationNotice(authed)
        else:
            raise NotImplementedError("require_auth does not know how to handle is_authed return type of %s" % (str(type(authed)),))
    
    return wrapper

def auth_or_die(environ):
    if not is_authed(environ):
        raise AuthenticationError

def simple_callback(func):
    """Shortcut for Twisted's Deferred expecting callbacks to return the deferred data."""
    
    @wraps(func)
    def wrapper(data):
        func(data)
        
        return data
    
    return wrapper

def make_deferred(data):
    """Wraps data into a deferred."""
    
    deferred = Deferred()
    
    deferred.callback(data)
    
    return deferred
