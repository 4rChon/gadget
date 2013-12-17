import glob
import os
import random
import importlib
from cStringIO import StringIO

from twisted.internet import reactor, protocol
from twisted.internet.defer import Deferred

from gadgetlib.Globals import Globals
from gadgetlib.handlers import require_auth, simple_callback, make_deferred

class SubprocessProtocol(protocol.ProcessProtocol):
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
        try:
            handler = self.handlers[cmd]
        except KeyError:
            self.send_message("No such command")
            
            return
        
        deferred = handler(cmd, args, environ)
        
        @simple_callback
        def callback(data):
            self.send_message(data)
        
        if deferred:
            deferred.addCallback(callback)
        
            return deferred
    
    def init_handlers(self):
        get_command_name = lambda name: name.split("handle_")[1]
        
        for name in dir(self):
            if name.startswith("handle_"):
                self.handlers.update({get_command_name(name): getattr(self, name)})
        
        internalHandlers = self.get_internal_handlers()
        
        for moduleName in internalHandlers:
            module = importlib.import_module("gadgetlib.handlers.%s" % moduleName)
            
            for name in dir(module):
                if name.startswith("handle_"):
                    func = getattr(module, name)
                    func = func.__get__(self, Commands) #bind the first argument
                    
                    self.handlers.update({get_command_name(name): func})
        
        fileCmds = [os.path.split(x)[1][:-3] for x in glob.glob("handlers/*.py")]
        
        for file in fileCmds:
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
    
    def get_auth_failure_msg(self):
        return random.choice(Globals.settings.AUTH_FAILURE_MESSAGES)
    
    def is_authed(self, environ):
        return any([environ.get("SKYPE_HANDLE", None) in x[0] for x in Globals.settings.ADMINISTRATORS])
    
    def sighup(self, signum, frame):
        self.handle_reload(None, None, {"SKYPE_HANDLE": Globals.settings.ADMINISTRATORS[0][0]})
    
    def sigterm(self, signum, frame):
        self.handle_quit(None, None, {"SKYPE_HANDLE": Globals.settings.ADMINISTRATORS[0][0]})
    
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
    
    #handlers
    
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
    
    def handle_help(self, cmd, args, environ):
        """!help [command name]\nShows you help n' stuff."""
        
        if len(args) > 0:
            name = args[0]
            
            try:
                handler = self.handlers[name]
            except KeyError:
                return make_deferred("No such command.")
            
            if handler == self.run_handler:
                return make_deferred("I don't know what {0} does.\ntry !{0} help".format(name))
            else:
                if hasattr(handler, "__doc__") and type(handler.__doc__) is str:
                    return make_deferred(handler.__doc__)
                else:
                    return make_deferred("I don't know what {0} does.".format(name))
        else:
            return make_deferred("I know about the following commands: " + ", ".join(self.handlers.keys()))
