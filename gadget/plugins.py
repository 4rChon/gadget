import random
from itertools import chain
from functools import wraps

from twisted.internet.defer import Deferred

from gadget import (WaitingForAuthenticationNotice, UnsupportedPlugin,
                    get_modules_in_package, get_modules_in_directory, get_setting)
from gadget.globals import Globals

def load_plugins():
    """Load all plugins."""
    
    modules = chain()
    
    for iterable in ([get_modules_in_package("gadget.default_plugins")] +
                     [get_modules_in_directory(dir) for dir in get_setting("PLUGIN_PATHS")]):
        modules = chain(modules, iterable)
    
    for module in modules:
        if hasattr(module, "initialize"):
            print "Loading plugin", module.__name__
            
            try:
                module.initialize()
                Globals.plugins.update({module.__name__: module})
            except UnsupportedPlugin as e:
                print "Plugin %s is unsupported: %s" % (module.__name__, e.message)
        else:
            print "Warning: plugin %s does not have an initialize function" % (module.__name__,)

def get_auth_failure_msg():
    return random.choice(get_setting("AUTH_FAILURE_MESSAGES"))

def is_authed(context):
    """Check whether a user is authenticated to run priviledged commands."""
    
    try:
        return context["protocol"].is_authed(context)
    except KeyError:
        print "Warning: is_authed called without protocol in context dictionary"
        
        return False

def require_auth(func):
    """Decorator for checking authentication before running a command."""
    
    @wraps(func)
    def wrapper(self, cmd, args, context):
        authed = is_authed(context)
        
        def complete(result):
            if not result:
                return make_deferred(get_auth_failure_msg())
            else:
                return func(self, cmd, args, context)
        
        if   type(authed) is bool:
            return complete(authed)
        elif authed.__class__ is Deferred: #type(Deferred()) returns <type 'instance'> (Deferred is an old-style class)
            authed.addCallback(complete) #default callback chaining behaviour returns the usual result from the command handler after verifying authentication
            
            raise WaitingForAuthenticationNotice(authed)
        else:
            raise NotImplementedError("require_auth does not know how to handle is_authed return type of %s" % (str(type(authed)),))
    
    return wrapper

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
