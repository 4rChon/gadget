from twisted.internet import reactor

def handle_patience(self, cmd, args, environ):
    """!patience\nBoost.Build kindly requests that you cool your tits."""
    
    def callback():
        self.send_message("...patience...")
    
    for x in range(0, 5):
        reactor.callLater(5*x, callback)
