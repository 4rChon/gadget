import os

from twisted.internet import reactor, protocol
from twisted.words.protocols.irc import IRCClient

from gadget import get_setting
from gadget.globals import Globals
from gadget.messages import subscribe, default_format, send_global, handle_message, make_context
from gadget.protocols import have_required_settings, parse_hostname

class IrcBot(IRCClient):
    """IRC protocol manager."""
    
    def __init__(self, factory, channels):
        self.factory = factory
        self.nickname = self.factory.nick
        self.channels = channels
    
    def signedOn(self):
        for channel in self.channels:
            self.join(channel)
    
    def noticed(self, user, channel, message):
        pass
    
    def privmsg(self, user, channel, message, action=False):
        name = user.split("!")[0]
        isGlobal = (channel in self.channels)
        
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
        send_global("[IRC] %s changed name to %s" % (old, new), self.factory)
    
    def userJoined(self, user, channel):
        if channel in self.channels:
            send_global("[IRC] %s joined" % (user,), self.factory)
    
    def userLeft(self, user, channel):
        if channel in self.channels:
            send_global("[IRC] %s left" % (user,), self.factory)
    
    def userQuit(self, user, reason):
        send_global("[IRC] %s quit (%s)" % (user, reason), self.factory)
    
    def userKicked(self, user, channel, kicker, reason):
        if channel in self.channels:
            send_global("[IRC] %s was kicked by %s (%s)" % (user, kicker, reason), self.factory)

class IRC(protocol.ClientFactory):
    """IRC connection manager."""
    
    PROTOCOL_NAME = "IRC"
    
    def __init__(self, nick, networks):
        self.nick = nick
        self.networks = networks
        self.clients = {}
        self.resolved = {}
        
        for network in networks:
            host, port = parse_hostname(network)
            client = IrcBot(self, networks[network])
            
            def capture(host, port, client): #hack around python's tricky scoping rules
                def callback(resolved):
                    addr = "%s:%s" % (resolved, port)
                    unresolvedAddr = "%s:%s" % (host, port)
                    client.address = unresolvedAddr
                    
                    self.resolved.update({addr: unresolvedAddr})
                    self.clients.update({unresolvedAddr: client})
                    reactor.connectTCP(resolved, port, self)
                
                return callback
            
            reactor.resolve(host).addCallback(capture(host, port, client))
        
        subscribe(self)
    
    def buildProtocol(self, addr):
        address = "%s:%s" % (addr.host, addr.port)
        
        print "[IRC] Connection made to", address
        
        return self.clients[self.resolved[address]]
    
    def clientConnectionLost(self, connector, reason):
        print "[IRC] Connection lost"
        
        connector.connect()
    
    def clientConnectionFailed(self, connector, reason):
        print "[IRC] Connection failed"
        
        reactor.callLater(16000, lambda: connector.connect())
    
    def send_message(self, context):
        client = None #???
        source = context.get("source")
        channels = []
        
        if   source:
            channels = [source]
        elif context.get("isGlobal"):
            channels = client.channels
        
        split = context.get("body").split(" ")
        cmd = split[0][1:].lower()
        body = " ".join(split[1:])
        func = client.msg
        
        if context.get("body").startswith("/"):
            if   cmd == "topic":
               func = client.topic
            elif cmd == "me":
                func = client.action
            else:
                print "[IRC] Error: don't know how to %s" % (cmd,)
                
                return
        else:
            body = context.get("body")
        
        for channel in channels:
            func(channel, body)
    
    def is_authed(self, context):
        return False #TODO
    
    def format_message(self, context):
        context["name"] = "\x02%s\x02" % (context.get("name"),)
        
        return default_format(context)

def build_protocol():
    if have_required_settings("NICKNAME", "IRC_CONNECTIONS"):
        irc = IRC(get_setting("NICKNAME"), get_setting("IRC_CONNECTIONS"))
        
        return irc
