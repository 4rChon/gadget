from gadgetlib.Globals import Globals

def handle_gc(self, cmd, args, context):
    """!gc [from __future__ import features]\nGlobalchat interface"""
    
    Globals.sven.send_message("%s: %s" % (context["name"], " ".join(args)))
