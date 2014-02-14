from twisted.internet import reactor, protocol

from gadget import get_setting
from gadget.protocols import have_required_settings, parse_hostname
from gadget.messages import send_global

class Echoer(protocol.DatagramProtocol):
    """Listens for datagrams, and sends them as messages."""
    
    def datagramReceived(self, data, (host, port)):
        send_global(data)

def build_protocol():
    if have_required_settings("ECHOER_BIND_ADDRESS"):
        host, port = parse_hostname(get_setting("ECHOER_BIND_ADDRESS"))
        echoer = Echoer()
        
        reactor.listenUDP(port, echoer, interface=host)
        
        return echoer
        
