import os

from twisted.internet import reactor, protocol
from twisted.words.protocols.irc import IRCClient

from gadget import get_setting
from gadget.globals import Globals

class TwitchBot(IRCClient):
    """IRC protocol manager."""
    
    def __init__(self, factory):
        self.factory = factory
        self.nickname = self.factory.nick
        self.password = self.factory.token
    
    def signedOn(self):
        for channel in get_setting("TWITCH_CHANNELS"):
            self.join(channel)
    
    def noticed(self, user, channel, message):
        pass #print user, channel, message
    
    def privmsg(self, user, channel, message, action=False):
        #no privmsgs pls
        if channel == self.factory.channel:
            name = user.split("!")[0]
            
            if action:
                #Globals.commands.send_message(u"[Twitch] *\x02%s\x02\u202d %s*" % (name, message), self)
                
                return
            else:
                pass #Globals.commands.send_message(u"[Twitch] \x02%s\x02\u202d: %s" % (name, message), self)
            
            if message.startswith(get_setting("COMMAND_PREFIX")):
                cmd, args = Globals.commands.parse_args(message)
                environ = Globals.commands.get_environment(self.factory, channel)
                environ["NAME"] = name
                
                Globals.commands(cmd, args, environ)
            else:
                Globals.commands.general(self.factory, user, message)
            
    
    def action(self, user, channel, message):
        self.privmsg(user, channel, message, True)

class Twitch(protocol.ClientFactory):
    """IRC connection manager."""
    
    def __init__(self, nick, token):
        self.nick = nick
        self.token = token
        self.client = None
        
        reactor.connectTCP("irc.twitch.tv", 6667, self)
    
    def buildProtocol(self, addr):
        print "[Twitch] Connection made"
        
        self.client = TwitchBot(self)
        
        return self.client
    
    def clientConnectionLost(self, connector, reason):
        print "[Twitch] Connection lost"
        
        connector.connect()
    
    def clientConnectionFailed(self, connector, reason):
        print "[Twitch] Connection failed"
        
        reactor.callLater(16000, lambda: connector.connect())
    
    def send_message(self, message):
        if not self.client:
            return
        
        if message.startswith("/"):
            args = message.split(" ")
            cmd = args[0][1:]
            joined = " ".join(args[1:]).replace("\n", "")
            
            if cmd.lower() == "me":
                self.client.action(self.channel, joined)
            else:
                print "[Twitch] Error: don't know how to %s" % (cmd,)
        else:
            self.client.say(self.channel, message)
    
    def is_authed(self, environ):
        return False #TODO
