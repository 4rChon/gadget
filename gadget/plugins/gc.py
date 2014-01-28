from gadget.Globals import Globals
from gadget.Commands import register_command

def handle_gc(self, cmd, args, context):
    """!gc [from __future__ import features]\nGlobalchat interface"""
    
    Globals.sven.send_message("%s: %s" % (context.get("name"), " ".join(args)))

register_command(handle_gc)
