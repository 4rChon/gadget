from gadget.globals import Globals
from gadget.commands import register_command

def handle_gc(self, cmd, args, context):
    """!gc [from __future__ import features]\nGlobalchat interface"""
    
    Globals.sven.send_message("%s: %s" % (context.get("name"), " ".join(args)))

register_command(handle_gc)
