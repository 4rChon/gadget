import random

from twisted.internet.defer import Deferred

from gadgetlib import AuthenticationError
from gadgetlib.Globals import Globals

def get_auth_failure_msg():
    return random.choice(Globals.settings.AUTH_FAILURE_MESSAGES)

def is_authed(environ):
    return any([environ.get("SKYPE_HANDLE", None) in x[0] for x in Globals.settings.ADMINISTRATORS])

def require_auth(func):
    """Decorator for checking authentication before running a command."""
    
    def wrapper(self, cmd, args, environ):
        if not is_authed(environ):
            return make_deferred(get_auth_failure_msg())
        else:
            return func(self, cmd, args, environ)
    
    return wrapper

def auth_or_die(environ):
    if not is_authed(environ):
        raise AuthenticationError

def simple_callback(func):
    """Shortcut for Twisted's Deferred expecting callbacks to return the deferred data."""
    
    def wrapper(data):
        func(data)
        
        return data
    
    return wrapper

def make_deferred(data):
    """Wraps data into a deferred."""
    
    deferred = Deferred()
    
    deferred.callback(data)
    
    return deferred
