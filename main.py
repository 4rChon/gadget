#!/usr/bin/env python
import sys
import os
import signal
import traceback

from twisted.internet import reactor
from twisted.internet.task import LoopingCall

from gadget.globals import Globals
from gadget.commands import Commands
from gadget.plugins import load_plugins
from gadget.protocols import load_protocols

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
    
    Globals.commands.init_commands()
    load_plugins()
    load_protocols()
    
    signal.signal(signal.SIGQUIT, sigquit)
    signal.signal(signal.SIGHUP, sighup)
    LoopingCall(reactor_step).start(1)
    reactor.run()
    
    if Globals.restart:
        sys.argv[0] = os.path.abspath(sys.argv[0])
        
        os.execv("/usr/bin/env", ["env", "python"] + sys.argv)

if __name__ == '__main__':
    main()
