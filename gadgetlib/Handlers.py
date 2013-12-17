import glob
import os
import random
from cStringIO import StringIO

from twisted.internet import reactor, protocol
from twisted.internet.defer import Deferred

from gadgetlib.Globals import Globals

class Handlers(object):
    """Source-agnostic message handlers."""
    
    class HandlerProtocol(protocol.ProcessProtocol):
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
        
        def callback(data):
            self.send_message(data)
        
        if deferred:
            deferred.addCallback(callback)
        
            return deferred
    
    def init_handlers(self):
        for member in dir(self):
            if member.startswith("handle_"):
                self.handlers.update({member.split("handle_")[1]: getattr(self, member)})
        
        fileCmds = [x.split("/")[1].split(".py")[0] for x in glob.glob("handlers/*.py")]
        
        for file in fileCmds:
            self.handlers.update({file: self.run_handler})
    
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
        
        return self.HandlerProtocol(cmdline, environ).deferred
    
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
    
    def deferred_wrap(self, data):
        deferred = Deferred()
        
        deferred.callback(data)
        
        return deferred
    
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
            self.send_message("fku")
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
            query = args[0]
            name = "handle_%s" % (query,)
            
            if hasattr(self, name):
                docs = getattr(self, name).__doc__
                
                if docs:
                    return self.deferred_wrap(docs)
                else:
                    return self.deferred_wrap("I don't know what %s does" % (query,))
            elif query in self.handlers.keys():
                return self.deferred_wrap("I don't know what %s does\nTry !%s help" % (query, query))
            else:
                return self.deferred_wrap("No such command")
        
        return self.deferred_wrap("I know about the following commands: " + ", ".join(self.handlers.keys()))
    
    def handle_reload(self, cmd, args, environ):
        if not self.is_authed(environ):
            return self.deferred_wrap(self.get_auth_failure_msg())
        
        Globals.running = False
        Globals.restart = True
    
    def handle_quit(self, cmd, args, environ):
        if not self.is_authed(environ):
            return self.deferred_wrap(self.get_auth_failure_msg())
        
        Globals.running = False
    
    def handle_pull(self, cmd, args, environ):
        if not self.is_authed(environ):
            return self.deferred_wrap(self.get_auth_failure_msg())
        
        deferred = self.HandlerProtocol("/usr/bin/git pull origin master".split(" "), os.environ.copy()).deferred
        
        deferred.addCallback(lambda *args: self.handle_reload(None, None, environ))
        
        return deferred
    
    def handle_topic(self, cmd, args, environ):
        if not self.is_authed(environ):
            return self.deferred_wrap(self.get_auth_failure_msg())
        
        self.send_message("/topic The %s Tavern" % (" ".join(args),))
    
    def handle_gc(self, cmd, args, environ):
        Globals.sven.send_message("%s: %s" % (environ[NAME], " ".join(args)))
    
    def handle_patience(self, cmd, args, environ):
        def callback():
            self.send_message("...patience...")
        
        for x in range(0, 5):
            reactor.callLater(5*x, callback)
