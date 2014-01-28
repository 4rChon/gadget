#!/usr/bin/env python
import sys
import os
import signal
import traceback

from twisted.internet import protocol, reactor
from twisted.internet.task import LoopingCall
from twisted.cred import portal as Portal, checkers
from twisted.conch import manhole, manhole_ssh

from gadget.globals import Globals
from gadget.commands import Commands
from gadget.messages import send_global
from gadget.Skype import Skype
from gadget.IRC import IRC
from gadget.GlobalChat import GlobalChat
from gadget.Twitch import Twitch

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

def manhole_factory(globals):
    realm = manhole_ssh.TerminalRealm()
    realm.chainedProtocolFactory.protocolFactory = lambda x: manhole.Manhole(globals)
    portal = Portal.Portal(realm)
    
    portal.registerChecker(checkers.InMemoryUsernamePasswordDatabaseDontUse(root=Globals.settings.MANHOLE_PASSWORD))
    
    return manhole_ssh.ConchFactory(portal)

def reactor_step():
    """Run every second by the reactor. Handles changes in running/retrySkypeAttach."""
    
    if Globals.running:
        if Globals.retrySkypeAttach:
            Globals.retrySkypeAttach = False
                            
            reactor.callInThread(skype.attach)
    else:
        print "Reloading..."
        
        reactor.stop()

def get_settings():
    try:
        import gadget_settings as settings
    except ImportError:
        import gadget_defaults as settings
        
        print "Warning: gadget_settings.py not found - creating with defaults"
        
        with open("gadget_settings.py", "w") as f:
            f.write("from gadget_defaults import *\n\n")
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

def sighup(signum, frame): #reload
    Globals.running = False
    Globals.restart = True

def sigquit(signum, frame): #quit
    Globals.running = False
    Globals.restart = False

def main():
    if not os.path.exists("data/"):
        os.mkdir("data/")
    
    Globals.settings = get_settings()
    Globals.commands = Commands()
    Globals.skype = Skype()
    cfg = Globals.settings
    
    Globals.commands.init_commands()
    
    if cfg.IRC_ADDRESS:
        Globals.irc = IRC(cfg.NICKNAME, *parse_hostname(cfg.IRC_ADDRESS), channels=cfg.IRC_CHANNELS)
    
    if cfg.GLOBALCHAT_ADDRESS:
        Globals.globalchat = GlobalChat(*parse_hostname(cfg.GLOBALCHAT_ADDRESS))
    
    if cfg.TWITCH_USERNAME:
        Globals.twitch = Twitch(cfg.TWITCH_USERNAME, cfg.TWITCH_OATH_TOKEN)
    
    if cfg.ECHOER_BIND_ADDRESS:
        host, port = parse_hostname(cfg.ECHOER_BIND_ADDRESS)
        
        reactor.listenUDP(port, Echoer(), interface=host)
    
    if cfg.MANHOLE_BIND_ADDRESS:
        host, port = parse_hostname(cfg.MANHOLE_BIND_ADDRESS)
        
        reactor.listenTCP(port, manhole_factory(globals()), interface=host)
    
    signal.signal(signal.SIGQUIT, sigquit)
    signal.signal(signal.SIGHUP, sighup)
    LoopingCall(reactor_step).start(1)
    reactor.run()
    
    if Globals.restart:
        sys.argv[0] = os.path.abspath(sys.argv[0])
        
        os.execv("/usr/bin/env", ["env", "python"] + sys.argv)

class Echoer(protocol.DatagramProtocol):
    """Listens for datagrams, and sends them as messages."""
    
    def datagramReceived(self, data, (host, port)):
        send_global(data)

if __name__ == '__main__':
    main()
