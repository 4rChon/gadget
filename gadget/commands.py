import glob
import os
import shlex
import re
import sys
from cStringIO import StringIO

from twisted.internet import reactor, protocol
from twisted.internet.defer import Deferred

from gadget import AuthenticationError, WaitingForAuthenticationNotice, get_setting
from gadget.globals import Globals
from gadget.messages import subscribe, send_message, Address
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
    def clean_environ(environment):
        """Filter non-string items from environment, as reactor.spawnProcess cannot handle them."""
        
        for k, v in environment.items():
            if type(v) not in [str, unicode]:
                environment.pop(k)
            
            if type(v) is unicode:
                environment[k] = v.encode("utf-8")
        
        return environment

class SendMessageProxy(object):
    """Wrapper for gadget.messages.send_message that uses the appropriate context for commands."""
    
    def __init__(self, context):
        self.context = context.copy()
        protocolName = self.context.get("protocol").PROTOCOL_NAME
        
        if self.context.get("destination").get(protocolName) == None:
            self.context.get("destination")[protocolName] = []
        
        self.context.update({"isFormatted": True})
        self.context.get("destination")\
            .get(protocolName)\
            .append(Address(protocolName, self.context.get("source"))) #send messages from command back to the source
        
    def __getattr__(self, attr):
        if attr == "send_message":
            return self.send_message
        else:
            return getattr(Globals.commands, attr)
    
    def send_message(self, msg):
        self.context.update({"body": msg})
        send_message(self.context)

class Commands(object):
    """Factory for management of command handlers."""
    
    def __init__(self):
        self.handlers = None
        self.scriptPaths = None
        
        subscribe(self.handle_incoming)
    
    def handle_incoming(self, context):
        """Scan incoming messages for commands."""
        
        body = context.get("body")
        
        if context.get("isEmote"):
            return
        
        if body.startswith(get_setting("COMMAND_PREFIX")):
            cmd, args = parse_args(body)
            
            self.handle_command(cmd, args, context)
            
            raise StopIteration
    
    def handle_command(self, cmd, args, context):
        """Execute a command."""
        
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
        """Load command scripts."""
        
        self.handlers = {}
        self.scriptPaths = {}
        regex = re.compile(r"(.*)/([\w\-]+)\.([\w\-]+)$")
        
        for folder in get_setting("COMMAND_PATHS"):
            folder = os.path.abspath(folder).replace("\\", "/")
            
            if not os.path.exists(folder):
                print "Warning: command folder %s doesn't exist" % (folder,)
                
                continue
            
            for file in glob.iglob("%s/*" % (folder,)):
                file = file.replace("\\", "/")
                parsed = regex.match(file)
                
                if parsed:
                    groups = parsed.groups()
                    
                    if groups[1] in self.handlers:
                        print "WARNING: command %s loaded more than once" % (groups[1],)
                    
                    self.handlers.update({groups[1]: self.run_handler})
                    self.scriptPaths.update({groups[1]: "%s/%s.%s" % (groups[0], groups[1], groups[2])})
    
    @staticmethod
    def run_handler(self, cmd, args, context):
        """Runs a handler script."""
        
        path = self.scriptPaths[cmd]
        cmdline = [path] + args
        context = context.copy()
        
        if sys.platform == "win32":
            if path.endswith(".py"): #we can at least run python scripts
                cmdline = [sys.executable] + cmdline
            else:
                return make_deferred("I can't run %s (I'm on Windows)" % (cmd,))
        
        context.update(os.environ)
        
        return SubprocessProtocol(cmdline, context).deferred
