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
from gadgetlib.Messages import subscribe_incoming, send_message
from gadgetlib.handlers import require_auth, simple_callback, make_deferred

def parse_args(body):
    """Parse a command message, returning command name and arguments."""
    
    args = shlex.split(body)
    cmd = args[0][1:].lower()
    args = args[1:]
    
    return cmd, args

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
            
            if type(v) is unicode:
                environ[k] = v.encode("utf-8")
        
        return environ

class Commands(object):
    """Factory for management of command handlers and related tasks."""
    
    def __init__(self):
        self.handlers = {}
        self.scriptPaths = {}
        self.currentContext = None
        
        self.init_handlers()
        subscribe_incoming(self.handle_incoming)
    
    def handle_incoming(self, context):
        """Scan incoming messages for commands."""
        
        body = context["body"]
        
        if context.get("isEmote"):
            return
        
        if body.startswith(Globals.settings.COMMAND_PREFIX):
            cmd, args = parse_args(body)
            
            self.handle_command(cmd, args, context)
            
            raise StopIteration
    
    def handle_command(self, cmd, args, context):
        self.currentContext = context
        
        try:
            handler = self.handlers[cmd]
        except KeyError:
            self.send_message("No such command")
            
            return
        
        try:
            deferred = handler(cmd, args, context)
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
                self.scriptPaths.update({groups[0]: "%s.%s" % (groups[0], groups[1])})
    
    def get_internal_handlers(self):
        internalHandlers = glob.glob("gadgetlib/handlers/*.py")
        
        for index, file in enumerate(internalHandlers):
            internalHandlers[index] = os.path.split(file)[1][:-3]
        
        internalHandlers.remove("__init__")
        
        return internalHandlers
    
    def run_handler(self, cmd, args, context):
        """Runs a handler script."""
        
        cmdline = ["./handlers/%s" % (self.scriptHandlers[cmd],)] + args
        
        context.update(os.context)
        
        return SubprocessProtocol(cmdline, context).deferred
    
    def send_message(self, msg):
        context = self.currentContext.copy()
        
        context.update({"isFormatted": True, "body": msg})
        send_message(context)
