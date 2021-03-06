import os

from twisted.internet import reactor

from gadget.commands import SubprocessProtocol, register_command
from gadget.globals import Globals
from gadget.plugins import require_auth, make_deferred, simple_callback, load_plugins
from gadget.messages import _subscribers, load_routes

@require_auth
def handle_reload(self, cmd, args, context):
    """!reload\nReload the list of commands."""
    
    essentialSubscribers = _subscribers[0:2] #_send_all_msgs and Commands.handle_incoming
    
    for _ in range(len(_subscribers)):
        _subscribers.pop(0)
    
    for x in essentialSubscribers:
        _subscribers.append(x)
    
    self.init_commands()
    load_plugins()
    load_routes()

@require_auth
def handle_restart(self, cmd, args, context):
    """!restart\nRestart me, bro!"""
    
    Globals.restart = True
    
    reactor.callLater(1, reactor.stop)
    
    return make_deferred("yessir")

@require_auth
def handle_quit(self, cmd, args, context):
    """!quit\nMake me go away!"""
    
    reactor.callLater(1, reactor.stop)
    
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
    
    return SubprocessProtocol(["/usr/bin/git"] + args, os.environ).deferred

def initialize():
    register_command(handle_reload)
    register_command(handle_restart)
    register_command(handle_quit)
    register_command(handle_pull)
    register_command(handle_git)
