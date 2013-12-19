from gadgetlib.Globals import Globals

def handle_gc(self, cmd, args, environ):
    """!gc [from __future__ import features]\nGlobalchat interface"""
    
    Globals.sven.send_message("%s: %s" % (environ[NAME], " ".join(args)))
