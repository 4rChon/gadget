import sys
import subprocess
import os
import glob
import random
import signal
import traceback

import Skype4Py as skype4py
from twisted.internet import protocol, reactor
from twisted.internet.task import LoopingCall
from twisted.protocols import basic
from twisted.words.protocols.irc import IRCClient
from twisted.cred import portal as Portal, checkers
from twisted.conch import manhole, manhole_ssh

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
retrySkypeAttach = False
skype = irc = sven = handlers = settings = None

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

def manhole_factory(globals):
    realm = manhole_ssh.TerminalRealm()
    realm.chainedProtocolFactory.protocolFactory = lambda x: manhole.Manhole(globals)
    portal = Portal.Portal(realm)
    
    portal.registerChecker(checkers.InMemoryUsernamePasswordDatabaseDontUse(root=settings.MANHOLE_PASSWORD))
    
    return manhole_ssh.ConchFactory(portal)

def reactor_step():
    """Run every second by the reactor. Handles changes in running/retrySkypeAttach."""
    
    global retrySkypeAttach
    
    if running:
        if retrySkypeAttach:
            retrySkypeAttach = False
                            
            skype.attach()
    else:
        print "Reloading..."
        
        reactor.stop()

def get_settings():
    try:
        import gadget_settings as settings
    except ImportError:
        print "Please create gadget_settings.py"
        
        raise SystemExit
    except Exception as e:
        print "Exception raised by gadget_settings.py:"
        
        traceback.print_exc()
        
        raise SystemExit
    
    return settings

def parse_hostname(string):
    try:
        split = string.split(":")
        split[1] = int(split[1])
        
        assert 0 <= split[1] <= 65535
        return split
    except IndexError:
        print "Error in settings:\n'%s' is not a valid hostname:port combination." % (string,)
        
        raise SystemExit
    except ValueError:
        print "Error in settings:\n%r is not a number." % (split[1],)
        
        raise SystemExit
    except AssertionError:
        print "Error in settings:\n%d is not a valid port. (try somewhere in 0-65535)" % (split[1],)
        
        raise SystemExit

def main():
    global settings, handlers, skype, irc, sven
    
    settings = get_settings()
    handlers = Handlers()
    skype = SkypeBot()
    
    if settings.IRC_HOST:
        irc = IrcFactory(settings.NICKNAME, *parse_hostname(settings.IRC_HOST), channel=settings.IRC_CHANNEL)
    
    if settings.GLOBALCHAT_HOST:
        sven = SvenChatFactory(*parse_hostname(settings.GLOBALCHAT_HOST))
    
    if settings.ECHOER_HOST:
        host, port = parse_hostname(settings.ECHOER_HOST)
        
        reactor.listenUDP(port, Echoer(), interface=host)
    
    if settings.MANHOLE_HOST:
        host, port = parse_hostname(settings.MANHOLE_HOST)
        
        reactor.listenTCP(port, manhole_factory(globals()), interface=host)
    
    signal.signal(signal.SIGTERM, handlers.sigterm)
    signal.signal(signal.SIGHUP, handlers.sighup)
    LoopingCall(reactor_step).start(1)
    reactor.run()
    
    if restart:
        sys.argv[0] = os.path.abspath(sys.argv[0])
        
        os.execv("/usr/bin/env", ["env", "python"] + sys.argv)

class Status(object):
    """Skype4Py aliases."""
    
    normal = skype4py.cusOnline
    busy = skype4py.cusDoNotDisturb
    waiting = skype4py.cusAway
    invisible = skype4py.cusInvisible
    
    @staticmethod
    def set(status):
        skype.skype.ChangeUserStatus(status)

class SkypeBot(object):
    """Skype API handler."""
    
    REATTACH_TIMEOUT = 60*60*1
    
    def __init__(self):
        self.get_skype()
        
        self.skype.Timeout = 5000
        self.skype.FriendlyName = settings.NICKNAME
        self.skype.Settings.AutoAway = False
        self.reattacher = LoopingCall(self.reattach)
        
        self.attach()
        self.reattacher.start(self.REATTACH_TIMEOUT)
    
    def get_skype(self):
        self.skype = skype4py.Skype(Transport='x11')
    
    def attach(self):
        global retrySkypeAttach
        
        
        try:
            self.skype.Attach()
            
            self.tavern = self.find_chat()
            self.skype.OnMessageStatus = self.message_handler
        except skype4py.errors.SkypeAPIError:
            print "[Skype] Failed to attach"
            
            retrySkypeAttach = True
    
    def reattach(self):
        print "[Skype] Reattaching"
        
        del self.skype
        
        self.get_skype()
        self.attach()
        reactor.callLater(self.REATTACH_TIMEOUT, self.reattach)
    
    def find_chat(self):
        for chat in self.skype.Chats:
            if self.skype.CurrentUserHandle in chat._Handle:
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
            
            
            if msg.Body.startswith(settings.COMMAND_PREFIX):
                Status.set(Status.busy)
                
                args = msg.Body.split(" ")
                cmd = args[0][1:].lower()
                environ = os.environ.copy()
                environ["NAME"] = msg.FromDisplayName
                environ["SKYPE_HANDLE"] = msg.FromHandle
                
                try:
                    Status.set(Status.waiting)
                    
                    result = handlers[cmd](cmd, args[1:], environ)
                except KeyError:
                    result = "No such command"
                
                if result:
                    send_message(result)
            else:
                handlers.general(self, msg.FromDisplayName, msg.Body)
            
            reactor.callLater(1, lambda: Status.set(Status.normal))
    
    def send_message(self, message):
        self.tavern.SendMessage(message)

class IrcBot(IRCClient):
    """IRC protocol manager."""
    
    def __init__(self, factory):
        self.factory = factory
        self.nickname = self.factory.nick
    
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
            
            
            if message.startswith(settings.COMMAND_PREFIX):
                Status.set(Status.busy)
                
                args = message.split(" ")
                cmd = args[0][1:].lower()
                environ = os.environ.copy()
                environ["NAME"] = name
                
                try:
                    Status.set(Status.waiting)
                    
                    result = handlers[cmd](cmd, args[1:], environ)
                except KeyError:
                    result = "No such command"
                
                if result:
                    send_message(result)
            else:
                handlers.general(self.factory, user, message)
            
            reactor.callLater(1, lambda: Status.set(Status.normal))
    
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
    """IRC connection manager."""
    
    def __init__(self, nick, host, port, channel):
        self.nick = nick
        self.channel = channel
        self.client = None
        
        reactor.connectTCP(host, port, self)
    
    def buildProtocol(self, addr):
        print "[IRC] Connection made"
        
        self.client = IrcBot(self)
        
        return self.client
    
    def clientConnectionLost(self, connector, reason):
        print "[IRC] Connection lost"
        
        connector.connect()
    
    def clientConnectionFailed(self, connector, reason):
        print "[IRC] Connection failed"
        
        reactor.callLater(16000, lambda: connector.connect())
    
    def send_message(self, message):
        if not self.client:
            return
        
        if message.startswith("/"):
            args = message.split(" ")
            cmd = args[0][1:]
            joined = " ".join(args[1:]).replace("\n", "")
            
            if cmd.lower() in "topic":
                self.client.topic(self.channel, joined)
            elif cmd.lower() == "me":
                self.client.action(self.channel, joined)
            else:
                print "[IRC] Error: don't know how to %s" % (cmd,)
        else:
            self.client.say(self.channel, message)

class Echoer(protocol.DatagramProtocol):
    """Listens for datagrams, and sends them as messages."""
    
    def datagramReceived(self, data, (host, port)):
        send_message(data)

class SvenChat(basic.LineReceiver):
    def __init__(self, factory):
        self.delimiter = "\n"
        self.factory = factory
    
    def connectionMade(self):
        self.sendLine("hello Gadget")
    
    def lineReceived(self, line):
        if line.startswith("<"):
            send_message(line)

class SvenChatFactory(protocol.ClientFactory):
    def __init__(self, host, port):
        reactor.connectTCP(host, port, self)
    
    def buildProtocol(self, addr):
        print "[GC] Connection made"
        
        self.client = SvenChat(self)
        
        return self.client
    
    def clientConnectionLost(self, connector, reason):
        print "[GC] Connection lost"
        
        connector.connect()
    
    def clientConnectionFailed(self, connector, reason):
        print "[GC] Connection failed"
        
        reactor.callLater(16000, lambda: connector.connect())
    
    def send_message(self, message):
        if type(message) is unicode:
            message = message.encode("utf-8")
        
        self.client.sendLine("< " + message)

class Handlers(object):
    """Source-agnostic message handlers."""
    
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
        """Runs a handler script."""
        
        if not os.path.exists("handlers/%s.py" % (cmd,)):
            return "Don't know how to %s" % (cmd,)
        
        if len(args) > 0:
            cmdline = "python handlers/%s.py %s" % (cmd, " ".join(args))
        else:
            cmdline = "python handlers/%s.py" % (cmd,)
        
        if type(environ["NAME"]) == unicode:
            environ["NAME"] = environ["NAME"].encode("utf-8")
        
        proc = subprocess.Popen(cmdline.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=environ)
        
        return proc.stdout.read() + proc.stderr.read()
    
    def get_auth_failure_msg(self):
        return random.choice(settings.AUTH_FAILURE_MESSAGES)
    
    def is_authed(self, environ):
        return any([environ.get("SKYPE_HANDLE", None) in x[0] for x in settings.ADMINISTRATORS])
    
    def sighup(self, signum, frame):
        self.handle_reload(None, None, {"SKYPE_HANDLE": settings.ADMINISTRATORS[0][0]})
    
    def sigterm(self, signum, frame):
        self.handle_quit(None, None, {"SKYPE_HANDLE": settings.ADMINISTRATORS[0][0]})
    
    def translate_sus(self, name):
        """Figure out what to say when someone says 'sus'"""
        
        for test, result in settings.SUS_TRANSLATIONS.iteritems():
            if test in name:
                return random.choice(result)
        
        return None
    
    #handlers
    
    def general(self, _, user, message):
        """Receives every message."""
        
        if   settings.NICKNAME.lower() == message.lower():
            send_message("sus")
        elif "sus" == message.lower():
            msg = self.translate_sus(user)
            
            if msg:
                send_message(msg)
            else:
                send_message("sus %s" % (user,))
        elif all([x in message.lower() for x in [settings.NICKNAME.lower(), "pls"]]): #GADGET PLS
            send_message(random.choice(settings.PLS_MESSAGES))
    
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
            return self.get_auth_failure_msg()
        
        running = False
        restart = True
    
    def handle_quit(self, cmd, args, environ):
        global running
        
        if not self.is_authed(environ):
            return self.get_auth_failure_msg()
        
        running = False
    
    def handle_pull(self, cmd, args, environ):
        if not self.is_authed(environ):
            return self.get_auth_failure_msg()
        
        proc = subprocess.Popen("/usr/bin/git pull origin master".split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        reactor.callLater(1, lambda: self.handle_reload(None, None, environ))
        
        return proc.stdout.read() + proc.stderr.read()
    
    def handle_topic(self, cmd, args, environ):
        if not self.is_authed(environ):
            return self.get_auth_failure_msg()
        
        send_message("/topic The %s Tavern" % (" ".join(args),))
    
    def handle_gc(self, cmd, args, environ):
        sven.send_message("%s: %s" % (environ[NAME], " ".join(args))
    
    def handle_patience(self, cmd, args, environ):
        def callback():
            send_message("...patience...")
        
        for x in range(0, 5):
            reactor.callLater(5*x, callback)

if __name__ == '__main__':
    try:
        main()
    except AttributeError as e:
        print "Setting '%s' is undefined" % (e.split("attribute ")[1][1:][:-1])
