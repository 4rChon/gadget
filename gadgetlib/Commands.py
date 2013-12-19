import glob
import os
import random
import importlib
from cStringIO import StringIO

from twisted.internet import reactor, protocol
from twisted.internet.defer import Deferred

from gadgetlib import AuthenticationError
from gadgetlib.Globals import Globals
from gadgetlib.handlers import require_auth, simple_callback, make_deferred

class SubprocessProtocol(protocol.ProcessProtocol):
    """Twisted-friendly subprocess."""
    
    def __init__(self, args, environment):
        self.deferred = Deferred()
        self.buffer = StringIO()
        
        reactor.spawnProcess(self, args[0], args, environment)
    
    def outReceived(self, data):
        self.buffer.write(data)
    
    def errReceived(self, data):
        self.outReceived(data)
    
    def processEnded(self, status):
        self.deferred.callback(self.buffer.getvalue())

class Commands(object):
    """Factory for management of command handlers and related tasks."""
    
    def __init__(self):
        self.handlers = {}
        
        self.init_handlers()
    
    def __call__(self, cmd, args, environ):
        """Called by protocol interfaces to notify us of command messages."""
        
        try:
            handler = self.handlers[cmd]
        except KeyError:
            self.send_message("No such command")
            
            return
        
        try:
            deferred = handler(cmd, args, environ)
        except AuthenticationError:
            deferred = make_deferred(get_auth_failure_msg())
        
        @simple_callback
        def callback(data):
            self.send_message(data)
        
        if deferred:
            deferred.addCallback(callback)
        
            return deferred
    
    def init_handlers(self):
        """Populate the dictionary of command handlers."""
        
        internalHandlers = self.get_internal_handlers()
        
        for moduleName in internalHandlers:
            module = importlib.import_module("gadgetlib.handlers.%s" % moduleName)
            
            for name in dir(module):
                if name.startswith("handle_"):
                    func = getattr(module, name)
                    func = func.__get__(self, Commands) #bind the first argument
                    
                    self.handlers.update({name.split("handle_")[1]: func})
        
        scriptHandlers = [os.path.split(x)[1][:-3] for x in glob.glob("handlers/*.py")]
        
        for file in scriptHandlers:
            self.handlers.update({file: self.run_handler})
    
    def get_internal_handlers(self):
        internalHandlers = glob.glob("gadgetlib/handlers/*.py")
        
        for index, file in zip(range(len(internalHandlers)), internalHandlers[:]):
            internalHandlers[index] = os.path.split(file)[1][:-3]
        
        internalHandlers.remove("__init__")
        
        return internalHandlers
    
    def run_handler(self, cmd, args, environ):
        """Runs a handler script."""
        
        if not os.path.exists("handlers/%s.py" % (cmd,)):
            return "Don't know how to %s" % (cmd,)
        
        if len(args) > 0:
            cmdline = "python handlers/%s.py %s" % (cmd, " ".join(args))
        else:
            cmdline = "python handlers/%s.py" % (cmd,)
        
        cmdline = cmdline.split(" ")
        
        if type(environ["NAME"]) == unicode:
            environ["NAME"] = environ["NAME"].encode("utf-8")
        
        return SubprocessProtocol(cmdline, environ).deferred
    
    def translate_sus(self, name):
        """Figure out what to say when someone says 'sus'"""
        
        for test, result in Globals.settings.SUS_TRANSLATIONS.iteritems():
            if test in name:
                return random.choice(result)
        
        return None
    
    def send_message(self, message, exclude=None):
        if type(message) is unicode:
            message = message.encode("utf-8")
        
        if exclude != Globals.skype:
            Globals.skype.send_message(message)
        
        if exclude != Globals.irc:
            if len(message) < 1500:
                Globals.irc.send_message(message)
            else:
                Globals.irc.send_message("error: output too long")
    
    def sighup(self, signum, frame):
        self.handlers.get("reload")(None, None, {"SKYPE_HANDLE": Globals.settings.ADMINISTRATORS[0][0]})
    
    def sigterm(self, signum, frame):
        self.handlers.get("quit")(None, None, {"SKYPE_HANDLE": Globals.settings.ADMINISTRATORS[0][0]})
    
    def general(self, _, user, message):
        """Receives every message."""
        
        if   Globals.settings.NICKNAME.lower() == message.lower():
            self.send_message(random.choice(Globals.settings.NAME_MESSAGES))
        elif "sus" == message.lower():
            msg = self.translate_sus(user)
            
            if msg:
                self.send_message(msg)
            else:
                self.send_message("sus %s" % (user,))
        elif all([x in message.lower() for x in [Globals.settings.NICKNAME.lower(), "pls"]]): #GADGET PLS
            self.send_message(random.choice(Globals.settings.PLS_MESSAGES))
