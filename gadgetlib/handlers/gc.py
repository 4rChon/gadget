from gadgetlib.Globals import Globals

def handle_gc(self, cmd, args, environ):
    Globals.sven.send_message("%s: %s" % (environ[NAME], " ".join(args)))
