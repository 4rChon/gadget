from twisted.internet import reactor

from gadget import get_setting, UnsupportedProtocol
from gadget.protocols import have_required_settings, parse_hostname

try:
    from twisted.cred import portal as Portal, checkers
    from twisted.conch import manhole, manhole_ssh
except ImportError as e:
    raise UnsupportedProtocol("Unable to import %s" % (e.message.split("module named ")[1],))

def manhole_factory():
    realm = manhole_ssh.TerminalRealm()
    realm.chainedProtocolFactory.protocolFactory = lambda x: manhole.Manhole({"__builtins__": __builtins__,
                                                                              "Globals": __import__("gadget.globals").Globals})
    portal = Portal.Portal(realm)
    
    portal.registerChecker(checkers.InMemoryUsernamePasswordDatabaseDontUse(root=get_setting("MANHOLE_PASSWORD")))
    
    return manhole_ssh.ConchFactory(portal)

def build_protocol():
    if have_required_settings("MANHOLE_BIND_ADDRESS", "MANHOLE_PASSWORD"):
        host, port = parse_hostname(get_setting("MANHOLE_BIND_ADDRESS"))
        manhole = manhole_factory()
        
        reactor.listenTCP(port, manhole, interface=host)
        
        return manhole
