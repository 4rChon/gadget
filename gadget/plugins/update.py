import os

from gadget.commands import SubprocessProtocol, register_command
from gadget.globals import Globals
from gadget.plugins import require_auth, make_deferred, simple_callback
from gadget.messages import _incomingSubscribers

@require_auth
def handle_reload(self, cmd, args, context):
    """!reload\nReload the list of commands."""
    
    essentialSubscribers = _incomingSubscribers[0:2] #_send_all_msgs and Commands.handle_incoming
    
    for _ in range(len(_incomingSubscribers)):
        _incomingSubscribers.pop(0)
    
    for x in essentialSubscribers:
        _incomingSubscribers.append(x)
    
    self.init_commands()

@require_auth
def handle_restart(self, cmd, args, context):
    """!restart\nRestart me, bro!"""
    
    Globals.running = False
    Globals.restart = True
    
    return make_deferred("yessir")

@require_auth
def handle_quit(self, cmd, args, context):
    """!quit\nMake me go away!"""
    
    Globals.running = False
    
    return make_deferred("later, bitches")

@require_auth
def handle_pull(self, cmd, args, context):
    """!pull\nUpdate from git"""
    
    deferred = handle_git(self, None, ["pull", "origin", "master"], context)
    
    @simple_callback
    def callback(data):
        self.handlers["restart"](None, None, None, context)
    
    deferred.addCallback(callback)
    
    return deferred

@require_auth
def handle_git(self, cmd, args, context):
    """!git <git commands>\nfor fixing 'dem pesky merge conflicts"""
    
    return SubprocessProtocol(["/usr/bin/git"] + args, os.environ.copy()).deferred

def initialize():
    register_command(handle_reload)
    register_command(handle_restart)
    register_command(handle_quit)
    register_command(handle_pull)
    register_command(handle_git)
