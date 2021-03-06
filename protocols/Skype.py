from twisted.internet import reactor
from twisted.internet.task import LoopingCall

from gadget import UnsupportedProtocol, get_setting
from gadget.messages import handle_message, make_context

try:
    import Skype4Py as skype4py
except ImportError:
    raise UnsupportedProtocol("Skype4Py is required")

class Skype(object):
    """Skype API handler."""
    
    REATTACH_TIMEOUT = 60*60*1
    PROTOCOL_NAME = "Skype"
    
    def __init__(self):
        self.skype = None
        self.reattacher = LoopingCall(self.reattach)
        
        self.reattacher.start(self.REATTACH_TIMEOUT)
    
    def make_skype(self):
        self.skype = skype4py.Skype(Transport='x11')
        self.skype.Timeout = 5000
        self.skype.FriendlyName = get_setting("NICKNAME")
        self.skype.OnMessageStatus = (lambda msg, status: reactor.callFromThread(self.message_handler, msg, status))
        self.skype.OnAttachmentStatus = (lambda status: reactor.callFromThread(self.attachment_status_handler, status))
    
    def attach(self):
        try:
            self.skype.Attach()
            self.skype.ChangeUserStatus(skype4py.cusOnline)
            
            self.accountName = self.skype.User().Handle
            self.skype.Settings.AutoAway = False
        except skype4py.errors.SkypeAPIError:
            print "[Skype] Failed to attach"
            
            reactor.callLater(self.REATTACH_TIMEOUT, self.attach)
    
    def reattach(self):
        print "[Skype] Reattaching"
        
        if self.skype:
            self.skype.__del__()
        
        del self.skype
        
        self.make_skype()
        self.attach()
        
        print "[Skype] Reattached"
    
    def find_chat(self, guid):
        for chat in self.skype.Chats:
            if chat._Handle == guid:
                return chat
        
        raise Exception("Unable to find skype conversation!")
    
    def message_handler(self, msg, status):
        if status == skype4py.cmsReceived:
            emote = False
            
            if msg.Type == skype4py.cmeEmoted:
                emote = True
            
            handle_message(
                make_context(
                    protocol=self,
                    source=msg.ChatName,
                    name=msg.FromDisplayName,
                    body=msg.Body,
                    skypeHandle=msg.FromHandle,
                    isEmote=emote,
                )
            )
    
    def attachment_status_handler(self, status):
        if status == skype4py.apiAttachAvailable:
            self.attach()
    
    def send_message(self, context):
        def send(context):
            chat = self.find_chat(context.get("destination"))
            
            try:
                chat.SendMessage(context.get("body"))
            except skype4py.errors.SkypeError:
                pass
        
        reactor.callInThread(send, context)
    
    def is_authed(self, context):
        return any([context.get("skypeHandle") in x[0] for x in get_setting("ADMINISTRATORS")])

def build_protocol():
    return Skype()
