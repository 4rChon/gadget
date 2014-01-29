import os

from twisted.internet import reactor, protocol
from twisted.words.protocols.irc import IRCClient

from gadget.globals import Globals
from gadget.messages import subscribe, default_format, send_global, handle_message, make_context

class IrcBot(IRCClient):
    """IRC protocol manager."""
    
    def __init__(self, factory):
        self.factory = factory
        self.nickname = self.factory.nick
    
    def signedOn(self):
        for channel in self.factory.channels:
            self.join(channel)
    
    def noticed(self, user, channel, message):
        pass
    
    def privmsg(self, user, channel, message, action=False):
        name = user.split("!")[0]
        isGlobal = (channel in self.factory.channels)
        
        handle_message(
            make_context(
                protocol=self.factory,
                source=channel if isGlobal else name,
                name=name,
                body=message,
                isEmote=action,
                isGlobal=isGlobal,
            )
        )
    
    def action(self, user, channel, message):
        self.privmsg(user, channel, message, True)
    
    def userRenamed(self, old, new):
        send_global("[IRC] %s changed name to %s" % (old, new))
    
    def userJoined(self, user, channel):
        if channel in self.factory.channels:
            send_global("[IRC] %s joined" % (user,))
    
    def userLeft(self, user, channel):
        if channel in self.factory.channels:
            send_global("[IRC] %s left" % (user,))
    
    def userQuit(self, user, reason):
        send_global("[IRC] %s quit (%s)" % (user, reason))
    
    def userKicked(self, user, channel, kicker, reason):
        if channel in self.factory.channels:
            send_global("[IRC] %s was kicked by %s (%s)" % (user, kicker, reason))

class IRC(protocol.ClientFactory):
    """IRC connection manager."""
    
    def __init__(self, nick, host, port, channels):
        self.nick = nick
        self.channels = channels
        self.client = None
        
        reactor.connectTCP(host, port, self)
        subscribe(self)
    
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
    
    def send_message(self, context):
        if not self.client:
            return
        
        source = context.get("source")
        channels = []
        
        if   source:
            channels = [source]
        elif context.get("isGlobal"):
            channels = self.channels
        
        cmd = context.get("body").split(" ")[0][1:].lower()
        func = self.client.msg
        
        if context.get("body").startswith("/"):
            if   cmd == "topic":
               func = self.client.topic
            elif cmd == "me":
                func = self.client.action
            else:
                print "[IRC] Error: don't know how to %s" % (cmd,)
        
        for channel in channels:
            func(channel, context.get("body"))
    
    def is_authed(self, context):
        return False #TODO
    
    def format_message(self, context):
        context["name"] = "\x02%s\x02" % (context.get("name"),)
        
        return default_format(context)
        
        
