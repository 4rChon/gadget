from gadgetlib.handlers import require_auth

@require_auth
def handle_topic(self, cmd, args, environ):
    self.send_message("/topic The %s Tavern" % (" ".join(args),))
