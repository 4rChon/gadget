from twisted.internet.defer import Deferred

def require_auth(func):
    def wrapper(self, cmd, args, environ):
        if not self.is_authed(environ):
            return make_deferred(self.get_auth_failure_msg())
        else:
            return func(self, cmd, args, environ)
    
    return wrapper

def simple_callback(func):
    def wrapper(data):
        func(data)
        
        return data
    
    return wrapper

def make_deferred(data):
    deferred = Deferred()
    
    deferred.callback(data)
    
    return deferred
