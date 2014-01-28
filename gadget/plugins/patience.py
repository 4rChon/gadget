from twisted.internet import reactor

from gadget.Commands import register_command

def handle_patience(self, cmd, args, context):
    """!patience\nBoost.Build kindly requests that you cool your tits."""
    
    def callback():
        self.send_message("...patience...")
    
    for x in range(0, 5):
        reactor.callLater(5*x, callback)

register_command(handle_patience)
