#!/usr/bin/env python
import sys
import os
import signal
import traceback

from twisted.internet import reactor

from gadget.globals import Globals
from gadget.commands import Commands
from gadget.plugins import load_plugins
from gadget.protocols import load_protocols
from gadget.messages import load_routes

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
    reactor.stop()
    
    Globals.restart = True

def sigquit(signum, frame): #quit
    reactor.stop()
    
    Globals.restart = False

def main():
    if not os.path.exists("data/"):
        os.mkdir("data/")
    
    Globals.settings = get_settings()
    Globals.commands = Commands()
    
    Globals.commands.init_commands()
    load_plugins()
    load_protocols()
    load_routes()
    
    try:
        signal.signal(signal.SIGQUIT, sigquit)
        signal.signal(signal.SIGHUP, sighup)
    except AttributeError: #windows compatability
        pass
    
    reactor.run()
    
    if Globals.restart:
        sys.argv[0] = os.path.abspath(sys.argv[0])
        
        os.execv("/usr/bin/env", ["env", "python"] + sys.argv)

if __name__ == '__main__':
    main()
