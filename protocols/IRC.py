from twisted.internet import reactor, protocol
from twisted.words.protocols.irc import IRCClient

from gadget import get_setting
from gadget.messages import default_format, send_global, handle_message, make_context
from gadget.protocols import have_required_settings, parse_hostname

class IrcBot(IRCClient):
    """IRC protocol manager."""
    
    def __init__(self, factory, network, channels):
        self.factory = factory
        self.network = network
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
        
        if channel in self.channels:
            source = channel
        else:
            source = '!' + name
                
        handle_message(
            make_context(
                protocol=self.factory,
                source=self.network + source,
                name=name,
                body=message,
                isEmote=action,
                isGlobal=isGlobal,
            )
        )
    
    def action(self, user, channel, message):
        self.privmsg(user, channel, message, True)
    
    def userRenamed(self, old, new):
        for channel in self.channels: #TODO: figure out which channels the user is in
            handle_message(
                make_context(
                    protocol=self.factory,
                    source=self.network+channel,
                    name=None,
                    body="[IRC] %s changed name to %s" % (old, new),
                    isFormatted=True,
                )
            )
    
    def userJoined(self, user, channel):
        if channel in self.channels:
            handle_message(
                make_context(
                    protocol=self.factory,
                    source=self.network+channel,
                    name=None,
                    body="[IRC] <%s> %s joined" % (channel, user,),
                    isFormatted=True,
                )
            )
    
    def userLeft(self, user, channel):
        if channel in self.channels:
            handle_message(
                make_context(
                    protocol=self.factory,
                    source=self.network+channel,
                    name=None,
                    body="[IRC] <%s> %s left" % (channel, user,),
                    isFormatted=True,
                )
            )
    
    def userQuit(self, user, reason):
        for channel in self.channels: #TODO: figure out which channels the user is in
            handle_message(
                make_context(
                    protocol=self.factory,
                    source=self.network+channel,
                    name=None,
                    body="[IRC] %s quit (%s)" % (user, reason),
                    isFormatted=True,
                )
            )
    
    def userKicked(self, user, channel, kicker, reason):
        if channel in self.channels:
            handle_message(
                make_context(
                    protocol=self.factory,
                    source=self.network+channel,
                    name=None,
                    body="[IRC] <%s> %s was kicked by %s (%s)" % (channel, user, kicker, reason),
                    isFormatted=True,
                )
            )

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
            client = IrcBot(self, network, networks[network])
            
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
    
    @staticmethod
    def parse_destination(context):
        destination = context.get("destination")
        isChannel = '#' in destination
        
        if isChannel:
            network, channel = destination.split("#")
            channel = '#' + channel
        else: #privmsg
            network, channel = destination.split("!")
        
        return isChannel, network, channel
    
    def send_message(self, context):
        isChannel, network, channel = self.parse_destination(context)
        client = self.clients.get(network, None)
        
        if not client:
            return
        
        split = context.get("body").split(" ")
        cmd = split[0][1:].lower()
        body = " ".join(split[1:])
        func = client.msg
        
        if context.get("body").startswith("/"):
            if   cmd == "topic":
               func = client.topic
            elif cmd == "me":
                func = client.describe
            else:
                print "[IRC] Error: don't know how to %s" % (cmd,)
                
                return
        else:
            body = context.get("body")
        
        func(channel, body.strip())
    
    def is_authed(self, context):
        return False #TODO
    
    def format_message(self, context):
        context["name"] = "\x02%s\x02" % (context.get("name"),) #bold names

def build_protocol():
    if have_required_settings("NICKNAME", "IRC_CONNECTIONS"):
        irc = IRC(get_setting("NICKNAME"), get_setting("IRC_CONNECTIONS"))
        
        return irc
