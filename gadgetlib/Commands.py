import glob
import os
import random
import importlib
import shlex
import re
from cStringIO import StringIO

from twisted.internet import reactor, protocol
from twisted.internet.defer import Deferred

from gadgetlib import AuthenticationError, WaitingForAuthenticationNotice
from gadgetlib.Globals import Globals
from gadgetlib.handlers import require_auth, simple_callback, make_deferred

class SubprocessProtocol(protocol.ProcessProtocol):
    """Twisted-friendly subprocess."""
    
    def __init__(self, args, environment):
        self.deferred = Deferred()
        self.buffer = StringIO()
        
        reactor.spawnProcess(self, args[0], args, self.clean_environ(environment))
    
    def outReceived(self, data):
        self.buffer.write(data)
    
    def errReceived(self, data):
        self.outReceived(data)
    
    def processEnded(self, status):
        self.deferred.callback(self.buffer.getvalue())
    
    @staticmethod
    def clean_environ(environ):
        """Filter non-string items from environ, as reactor.spawnProcess cannot handle them."""
        
        for k, v in environ.items():
            if type(v) not in [str, unicode]:
                environ.pop(k)
        
        return environ

class Commands(object):
    """Factory for management of command handlers and related tasks."""
    
    def __init__(self):
        self.handlers = {}
        self.scriptHandlers = {}
        
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
        except WaitingForAuthenticationNotice as e:
            deferred = e.args[0]
        
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
        
        regex = re.compile(r"handlers/([\w\-]+)\.([\w\-]+)$")
        
        for file in glob.iglob("handlers/*"):
            parsed = regex.match(file)
            
            if parsed:
                groups = parsed.groups()
                
                self.handlers.update({groups[0]: self.run_handler})
                self.scriptHandlers.update({groups[0]: "%s.%s" % (groups[0], groups[1])})
    
    def get_internal_handlers(self):
        internalHandlers = glob.glob("gadgetlib/handlers/*.py")
        
        for index, file in enumerate(internalHandlers):
            internalHandlers[index] = os.path.split(file)[1][:-3]
        
        internalHandlers.remove("__init__")
        
        return internalHandlers
    
    def run_handler(self, cmd, args, environ):
        """Runs a handler script."""
        
        cmdline = "./handlers/%s" % (self.scriptHandlers[cmd],)
        
        if len(args) > 1:
            cmdline += " %s" % (" ".join(args),) #TODO: better solution
        
        cmdline = shlex.split(cmdline)
        
        if type(environ["NAME"]) == unicode:
            environ["NAME"] = environ["NAME"].encode("utf-8")
        
        environ.update(os.environ)
        
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
    
    @staticmethod
    def parse_args(message):
        """Parse a command message, returning command name and arguments."""
        
        args = shlex.split(message)
        cmd = args[0][1:].lower()
        args = args[1:]
        
        return cmd, args
    
    @staticmethod
    def get_environment(protocol, sourceInfo=None):
        """Returns environment (message context) dict."""
        
        environ = {"protocol": protocol, "source": sourceInfo}
        
        return environ
    
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
