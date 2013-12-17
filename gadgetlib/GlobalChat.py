from twisted.internet import reactor, protocol
from twisted.protocols import basic

class GlobalChatProtocol(basic.LineReceiver):
    def __init__(self, factory):
        self.delimiter = "\n"
        self.factory = factory
    
    def connectionMade(self):
        self.sendLine("hello Gadget")
    
    def lineReceived(self, line):
        if line.startswith("<"):
            Globals.commands.send_message(line)

class GlobalChatFactory(protocol.ClientFactory):
    def __init__(self, host, port):
        reactor.connectTCP(host, port, self)
    
    def buildProtocol(self, addr):
        print "[GC] Connection made"
        
        self.client = GlobalChatProtocol(self)
        
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
    
    def is_authed(self, environ):
        return False #TODO: needs protocol support
