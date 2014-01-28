import glob
import os
import importlib
import shlex
import re
import pkgutil
import traceback
from cStringIO import StringIO

from twisted.internet import reactor, protocol
from twisted.internet.defer import Deferred

from gadget import AuthenticationError, WaitingForAuthenticationNotice
from gadget.globals import Globals
from gadget.messages import subscribe_incoming, send_message
from gadget.plugins import simple_callback, make_deferred

def parse_args(body):
    """Parse a command message, returning command name and arguments."""
    
    args = shlex.split(body)
    cmd = args[0][1:].lower()
    args = args[1:]
    
    return cmd, args

def register_command(func, name=None):
    if not name:
        try:
            name = func.__name__.split("handle_")[1]
        except (AttributeError, IndexError):
            raise NameError("No name given and name cannot be deduced from function name.")
    
    Globals.commands.handlers.update({name: func})

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

class SendMessageProxy(object):
    """Wrapper for Messages.send_message that uses the appropriate context."""
    
    def __init__(self, context):
        self.context = context
        
    def __getattr__(self, attr):
        if attr == "send_message":
            return self.send_message
        else:
            return getattr(Globals.commands, attr)
    
    def send_message(self, msg):
        context = self.context.copy()
        
        context.update({"isFormatted": True, "body": msg})
        send_message(context)

class Commands(object):
    """Factory for management of command handlers and related tasks."""
    
    def __init__(self):
        self.handlers = None
        self.scriptPaths = None
        
        subscribe_incoming(self.handle_incoming)
    
    def handle_incoming(self, context):
        """Scan incoming messages for commands."""
        
        body = context.get("body")
        
        if context.get("isEmote"):
            return
        
        if body.startswith(Globals.settings.COMMAND_PREFIX):
            cmd, args = parse_args(body)
            
            self.handle_command(cmd, args, context)
            
            raise StopIteration
    
    def handle_command(self, cmd, args, context):
        proxy = SendMessageProxy(context)
        
        try:
            handler = self.handlers[cmd]
        except KeyError:
            proxy.send_message("No such command")
            
            return
        
        try:
            deferred = handler(proxy, cmd, args, context)
        except AuthenticationError:
            deferred = make_deferred(get_auth_failure_msg())
        except WaitingForAuthenticationNotice as e:
            deferred = e.args[0]
        
        @simple_callback
        def callback(data):
            proxy.send_message(data)
        
        if deferred:
            deferred.addCallback(callback)
            
            return deferred
    
    def init_commands(self):
        self.handlers = {}
        self.scriptPaths = {}
        
        #load plugins
        for moduleName in self.get_plugin_modules():
            try:
                plugin = importlib.import_module("gadget.plugins.%s" % moduleName)
                
                if hasattr(plugin, "initialize"):
                    plugin.initialize()
                else:
                    print "Warning: plugin %s does not have an initialize function" % (moduleName,)
            except Exception as e:
                print "Exception raised when loading plugin %s:" % (moduleName,)
                
                traceback.print_exc()
        
        #load command scripts
        if not os.path.exists("commands"):
            return
        
        regex = re.compile(r"commands/([\w\-]+)\.([\w\-]+)$")
        
        for file in glob.iglob("commands/*"):
            parsed = regex.match(file)
            
            if parsed:
                groups = parsed.groups()
                
                self.handlers.update({groups[0]: self.run_handler})
                self.scriptPaths.update({groups[0]: "%s.%s" % (groups[0], groups[1])})
    
    def get_plugin_modules(self):
        import gadget.plugins as package
        
        path = os.path.dirname(package.__file__)
        plugins = []
        
        for _, name, isPkg in pkgutil.iter_modules([path]):
            if not isPkg:
                yield name
    
    @staticmethod
    def run_handler(self, cmd, args, context):
        """Runs a handler script."""
        
        cmdline = ["./commands/%s" % (self.scriptPaths[cmd],)] + args
        context = context.copy()
        
        context.update(os.environ)
        
        return SubprocessProtocol(cmdline, context).deferred
