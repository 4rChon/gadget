import pdb
import time
import subprocess
import os
import sys
import glob
import string
import random
import code
import signal

import Skype4Py as skype4py
from twisted.internet import protocol, reactor
from twisted.words.protocols.irc import IRCClient

ADMINISTRATOR_NAME = "mr.angry"
AUTH_FAILURE_MESSAGES = [
    "I am a strong black woman who don't need no man",
    "no",
    "lol",
    "ok, I'll get right on that",
    "how about no?",
    "maybe tomorrow",
    "I don't like your face, so no",
]
PLS_MESSAGES = [
    "NO!",
    "it wasn't me",
    "shitty programming?",
    "this is all Yop's fault, I swear!",
    "oops",
    "pls urself",
    "no!",
    "nyet",
    "nein",
]
SUS_TRANSLATIONS = {
    (lambda name: "goppend" in name): ["gopsus", "hi goppend", "heil goppend"],
    (lambda name: "centipede" in name): ["susipede", "centisus", "shouldn't you be at the bakery?"],
    (lambda name: "KEEEAAGGH" in name): ["kegsus", "sus keg", "where the hell is micronesia?"],
    (lambda name: "Administrator" in name): ["zekesus", "sus zekin"],
    (lambda name: "RimShooter" in name): ["rimsus", "susshooter", "ramshoot", "ramscoop", "rimjob mcbimbob", "riddle diddle jim jam"],
    (lambda name: "Ben" in name): ["benson", "bensus", "bendy sus\nBENDY! BENDY!! BENDY! BENDY!!"],
    (lambda name: "Yoplitein" in name): ["yopsus", "yop is fgt"],
}

realStdout = sys.stdout
realStderr = sys.stderr

def make_replacement(file):
    class wrapper(object):
        @staticmethod
        def write(*args):
            file.write(*args)
            file.flush()
    
    return wrapper()

sys.stdout = make_replacement(realStdout)
sys.stderr = make_replacement(realStderr)

running = True
restart = False
retry = False
skype = irc = handlers = None

def send_message(message, exclude=None):
    if type(message) is unicode:
        message = message.encode("utf-8")
    
    if exclude != skype:
        skype.send_message(message)
    
    if exclude != irc:
        if len(message) < 1500:
            irc.send_message(message)
        else:
            irc.send_message("error: output too long")

class SkypeBot(object):
    def __init__(self):
        self.skype = skype4py.Skype(Transport='x11')
        self.skype.Timeout = 5000
        self.skype.FriendlyName = "Gadget"
        
        self.attach()
    
    def attach(self):
        global retry
        
        print "Attempting to attach to skype"
        
        try:
            self.skype.Attach()
            
            self.tavern = self.find_chat()
            self.skype.OnMessageStatus = self.message_handler
        except skype4py.errors.SkypeAPIError:
            retry = True
    
    def find_chat(self):
        for chat in self.skype.Chats:
            if "yop.lit.ein" in chat._Handle:
                continue
            else:
                return chat
        
        raise Exception("Unable to find tavern!")
    
    def message_handler(self, msg, status):
        if status == skype4py.cmsReceived:
            if msg.Type == skype4py.cmeEmoted:
                send_message(u"[Skype] *\x02%s\x02\u202d %s*" % (msg.FromDisplayName.replace("\u202e", ""), msg.Body), skype)
                
                return
            else:
                send_message(u"[Skype] \x02%s\x02\u202d: %s" % (msg.FromDisplayName, msg.Body), skype)
            
            if msg.Body.startswith("!"):
                args = msg.Body.split(" ")
                cmd = args[0][1:].lower()
                environ = os.environ.copy()
                environ["NAME"] = msg.FromDisplayName
                environ["SKYPE_HANDLE"] = msg.FromHandle
                
                try:
                    result = handlers[cmd](cmd, args[1:], environ)
                except KeyError:
                    result = "No such command"
                
                if result:
                    send_message(result)
            else:
                handlers.general(self, msg.FromDisplayName, msg.Body)
    
    def send_message(self, message):
        self.tavern.SendMessage(message)

class IrcBot(IRCClient):
    def __init__(self, factory):
        self.factory = factory
        self.nickname = self.factory.nick
    
    #def connectionMade(self):
    #    IRCClient.connectionMade(self)
    
    #I have no idea why this isn't included in IRCClient
    #(stolen from http://twistedmatrix.com/trac/browser/tags/releases/twisted-8.2.0/twisted/words/protocols/irc.py#L123)
    def send_command(self, command, *parameter_list, **prefix):
        """Send a line formatted as an IRC message.

        First argument is the command, all subsequent arguments
        are parameters to that command.  If a prefix is desired,
        it may be specified with the keyword argument 'prefix'.
        """

        if not command:
            raise ValueError, "IRC message requires a command. (" + repr(command) + ")"

        if ' ' in command or command[0] == ':':
            # Not the ONLY way to screw up, but provides a little
            # sanity checking to catch likely dumb mistakes.
            raise ValueError, "Somebody screwed up, 'cuz this doesn't" \
                  " look like a command to me: %s" % command

        line = string.join([command] + list(parameter_list))
        if prefix.has_key('prefix'):
            line = ":%s %s" % (prefix['prefix'], line)
        
        print line
        
        self.sendLine(line)

        if len(parameter_list) > 15:
            log.msg("Message has %d parameters (RFC allows 15):\n%s" %
                    (len(parameter_list), line))
    
    def signedOn(self):
        self.join(self.factory.channel)
    
    def noticed(self, user, channel, message):
        pass #print user, channel, message
    
    def privmsg(self, user, channel, message, action=False):
        #no privmsgs pls
        if channel == self.factory.channel:
            name = user.split("!")[0]
            
            if action:
                send_message(u"[IRC] *\x02%s\x02\u202d %s*" % (name, message), irc)
                
                return
            else:
                send_message(u"[IRC] \x02%s\x02\u202d: %s" % (name, message), irc)
            
            if message.startswith("!"):
                args = message.split(" ")
                cmd = args[0][1:].lower()
                environ = os.environ.copy()
                environ["NAME"] = name
                
                try:
                    result = handlers[cmd](cmd, args[1:], environ)
                except KeyError:
                    result = "No such command"
                
                if result:
                    send_message(result)
            else:
                handlers.general(self.factory, user, message)
    
    def action(self, user, channel, message):
        self.privmsg(user, channel, message, True)
    
    def userRenamed(self, old, new):
        send_message("[IRC] %s changed name to %s" % (old, new), irc)
    
    def userJoined(self, user, channel):
        if channel == self.factory.channel:
            send_message("[IRC] %s joined" % (user,), irc)
    
    def userLeft(self, user, channel):
        if channel == self.factory.channel:
            send_message("[IRC] %s left" % (user,), irc)
    
    def userQuit(self, user, reason):
        send_message("[IRC] %s quit (%s)" % (user, reason), irc)
    
    def userKicked(self, user, channel, kicker, reason):
        if channel == self.factory.channel:
            send_message("[IRC] %s was kicked by %s (%s)" % (user, kicker, reason), irc)

class IrcFactory(protocol.ClientFactory):
    def __init__(self, nick, host, port, channel):
        self.nick = nick
        self.channel = channel
        self.client = None
        
        self.reactor_step()
        reactor.connectTCP(host, port, self)
    
    def reactor_step(self):
        global retry
        
        if running:
            if retry:
                retry = False
                                
                skype.attach()
            
            reactor.callLater(1, self.reactor_step)
        else:
            print "Reloading..."
            
            reactor.stop()
    
    def buildProtocol(self, addr):
        print "Connection made"
        
        self.client = IrcBot(self)
        
        return self.client
    
    def clientConnectionLost(self, connector, reason):
        print "Connection lost"
        
        connector.connect()
    
    def clientConnectionFailed(self, connector, reason):
        print "Connection failed"
        
        reactor.callLater(16000, lambda: connector.connect())
    
    def send_message(self, message):
        if not self.client:
            return
        
        if message.startswith("/"):
            args = message.split(" ")
            cmd = args[0][1:]
            
            if cmd.lower() == "topic":
                self.client.topic(self.channel, " ".join(args[1:]).replace("\n", ""))
                
                return;
            
            self.client.send_command(cmd, *(args[1:]))
        else:
            self.client.say(self.channel, message)

class Handlers(object):
    def __init__(self):
        self.handlers = {}
        
        self.init_handlers()
    
    def __getitem__(self, value):
        return self.handlers[value]
    
    def init_handlers(self):
        for member in dir(self):
            if member.startswith("handle_"):
                self.handlers.update({member.split("handle_")[1]: getattr(self, member)})
        
        fileCmds = [x.split("/")[1].split(".py")[0] for x in glob.glob("handlers/*.py")]
        
        for file in fileCmds:
            self.handlers.update({file: self.run_handler})
    
    def run_handler(self, cmd, args, environ):
        if not os.path.exists("handlers/%s.py" % (cmd,)):
            return "Don't know how to %s" % (cmd,)
        
        if len(args) > 0:
            cmdline = "python handlers/%s.py %s" % (cmd, " ".join(args))
        else:
            cmdline = "python handlers/%s.py" % (cmd,)
        
        proc = subprocess.Popen(cmdline.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=environ)
        
        return proc.stdout.read() + proc.stderr.read()
    
    def auth_failure(self):
        return random.choice(AUTH_FAILURE_MESSAGES)
    
    def is_authed(self, environ):
        return environ.get("SKYPE_HANDLE", None) == ADMINISTRATOR_NAME
    
    def sighup(self, signum, frame):
        self.handle_reload(None, None, {"SKYPE_HANDLE": ADMINISTRATOR_NAME})
    
    def translate_sus(self, name):
        for test, result in SUS_TRANSLATIONS.iteritems():
            if test(name):
                return random.choice(result)
        
        return None
    
    #receives every message
    def general(self, _, user, message):
        if   "gadget" == message.lower():
            send_message("sus")
        elif "sus" == message.lower():
            msg = self.translate_sus(user)
            
            if msg:
                send_message(msg)
            else:
                send_message("sus %s" % (user,))
        elif all([x in message.lower() for x in ["gadget", "pls"]]): #GADGET PLS
            send_message(random.choice(PLS_MESSAGES))
        #elif "gadget" in message.lower():
        #    randChars = [chr(x) for x in range(ord('a'), ord('z'))]
        #    
        #    random.shuffle(randChars)
        #    send_message("".join(randChars))
    
    def handle_help(self, cmd, args, environ):
        """!help [command name]\nShows you help n' stuff."""
        
        if len(args) > 0:
            query = args[0]
            name = "handle_%s" % (query,)
            
            if hasattr(self, name):
                docs = getattr(self, name).__doc__
                
                if docs:
                    return docs
                else:
                    return "I don't know what %s does" % (query,)
            elif query in self.handlers.keys():
                return "I don't know what %s does\nTry !%s help" % (query, query)
            else:
                return "No such command"
        
        return "I know about the following commands: " + ", ".join(self.handlers.keys())
    
    def handle_reload(self, cmd, args, environ):
        global running, restart
        
        if not self.is_authed(environ):
            return self.auth_failure()
        
        running = False
        restart = True
    
    def handle_quit(self, cmd, args, environ):
        global running
        
        if not self.is_authed(environ):
            return self.auth_failure()
        
        running = False
    
    def handle_interpreter(self, cmd, args, environ):
        if not self.is_authed(environ):
            return self.auth_failure()
        
        code.interact(local=globals())
    
    def handle_pull(self, cmd, args, environ):
        if not self.is_authed(environ):
            return self.auth_failure()
        
        proc = subprocess.Popen("/usr/bin/git pull origin master".split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        reactor.callLater(1, lambda: self.handle_reload(None, None, environ))
        
        return proc.stdout.read() + proc.stderr.read()
    
if __name__ == "__main__":
    handlers = Handlers()
    skype = SkypeBot()
    irc = IrcFactory("Gadget", "localhost", 6667, "#tavern")
    
    signal.signal(signal.SIGHUP, handlers.sighup)
    
    reactor.run()
    
    if restart:
        sys.argv[0] = os.path.abspath(sys.argv[0])
        
        os.execv("/usr/bin/env", ["env", "python"] + sys.argv)
