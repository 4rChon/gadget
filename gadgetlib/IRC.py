import os

from twisted.internet import reactor, protocol
from twisted.words.protocols.irc import IRCClient

from gadgetlib.Globals import Globals

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
                Globals.handlers.send_message(u"[IRC] *\x02%s\x02\u202d %s*" % (name, message), irc)
                
                return
            else:
                Globals.handlers.send_message(u"[IRC] \x02%s\x02\u202d: %s" % (name, message), irc)
            
            if message.startswith(Globals.settings.COMMAND_PREFIX):
                args = message.split(" ")
                cmd = args[0][1:].lower()
                environ = os.environ.copy()
                environ["NAME"] = name
                
                Globals.handlers(cmd, args[1:], environ)
            else:
                Globals.handlers.general(self.factory, user, message)
            
    
    def action(self, user, channel, message):
        self.privmsg(user, channel, message, True)
    
    def userRenamed(self, old, new):
        Globals.handlers.send_message("[IRC] %s changed name to %s" % (old, new), irc)
    
    def userJoined(self, user, channel):
        if channel == self.factory.channel:
            Globals.handlers.send_message("[IRC] %s joined" % (user,), irc)
    
    def userLeft(self, user, channel):
        if channel == self.factory.channel:
            Globals.handlers.send_message("[IRC] %s left" % (user,), irc)
    
    def userQuit(self, user, reason):
        Globals.handlers.send_message("[IRC] %s quit (%s)" % (user, reason), irc)
    
    def userKicked(self, user, channel, kicker, reason):
        if channel == self.factory.channel:
            Globals.handlers.send_message("[IRC] %s was kicked by %s (%s)" % (user, kicker, reason), irc)

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
    
    def is_authed(self, environ):
        return False #TODO
