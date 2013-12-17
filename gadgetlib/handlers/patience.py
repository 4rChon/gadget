from twisted.internet import reactor

def handle_patience(self, cmd, args, environ):
    def callback():
        self.send_message("...patience...")
    
    for x in range(0, 5):
        reactor.callLater(5*x, callback)
