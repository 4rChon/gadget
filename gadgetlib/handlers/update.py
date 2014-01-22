import os
import shlex

from gadgetlib.Commands import SubprocessProtocol
from gadgetlib.Globals import Globals
from gadgetlib.handlers import require_auth, make_deferred, simple_callback

@require_auth
def handle_reload(self, cmd, args, environ):
    """!reload\nReload me, bro!"""
    
    Globals.running = False
    Globals.restart = True
    
    return make_deferred("yessir")

@require_auth
def handle_quit(self, cmd, args, environ):
    """!quit\nMake me go away!"""
    
    Globals.running = False
    
    return make_deferred("later, bitches")

@require_auth
def handle_pull(self, cmd, args, environ):
    """!pull\nUpdate from git"""
    
    deferred = handle_git(self, None, ["pull", "origin", "master"], environ)
    
    @simple_callback
    def callback(data):
        self.handlers["reload"](None, None, environ)
    
    deferred.addCallback(callback)
    
    return deferred

@require_auth
def handle_git(self, cmd, args, environ):
    """!git <git commands>\nfor fixing 'dem pesky merge conflicts"""
    
    return SubprocessProtocol(["/usr/bin/git"] + args, os.environ.copy()).deferred
