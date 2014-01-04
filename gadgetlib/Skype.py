import os

import Skype4Py as skype4py
from twisted.internet import reactor
from twisted.internet.task import LoopingCall

from gadgetlib.Globals import Globals

class SkypeBot(object):
    """Skype API handler."""
    
    REATTACH_TIMEOUT = 60*60*1
    
    def __init__(self):
        self.skype = None
        self.reattacher = LoopingCall(self.reattach)
        
        self.reattacher.start(self.REATTACH_TIMEOUT)
    
    def make_skype(self):
        self.skype = skype4py.Skype(Transport='x11')
        self.skype.Timeout = 5000
        self.skype.FriendlyName = Globals.settings.NICKNAME
        self.skype.OnMessageStatus = (lambda msg, status: reactor.callFromThread(self.message_handler, msg, status))
        self.skype.OnAttachmentStatus = (lambda status: reactor.callFromThread(self.attachment_status_handler, status))
    
    def attach(self):
        global retrySkypeAttach
        
        try:
            self.skype.Attach()
            
            self.tavern = self.find_chat()
            self.skype.Settings.AutoAway = False
        except skype4py.errors.SkypeAPIError:
            print "[Skype] Failed to attach"
            
            retrySkypeAttach = True
    
    def reattach(self):
        print "[Skype] Reattaching"
        
        if self.skype:
            self.skype.__del__()
        
        del self.skype
        
        self.make_skype()
        self.attach()
        
        print "[Skype] Reattached"
    
    def find_chat(self):
        for chat in self.skype.Chats:
            if chat._Handle == Globals.settings.SKYPE_CONVERSATION_ID:
                return chat
        
        raise Exception("Unable to find skype conversation!")
    
    def message_handler(self, msg, status):
        if status == skype4py.cmsReceived:
            if msg.Type == skype4py.cmeEmoted:
                Globals.commands.send_message(u"[Skype] *\x02%s\x02\u202d %s*" % (msg.FromDisplayName.replace("\u202e", ""), msg.Body), self)
                
                return
            else:
                Globals.commands.send_message(u"[Skype] \x02%s\x02\u202d: %s" % (msg.FromDisplayName, msg.Body), self)
            
            if msg.Body.startswith(Globals.settings.COMMAND_PREFIX):
                args = msg.Body.split(" ")
                cmd = args[0][1:].lower()
                environ = os.environ.copy()
                environ["NAME"] = msg.FromDisplayName
                environ["SKYPE_HANDLE"] = msg.FromHandle
                
                Globals.commands(cmd, args[1:], environ)
            else:
                Globals.commands.general(self, msg.FromDisplayName, msg.Body)
    
    def attachment_status_handler(self, status):
        global retrySkypeAttach
        
        if status == skype4py.apiAttachAvailable:
            retrySkypeAttach = True
    
    def send_message(self, message):
        reactor.callInThread(self.tavern.SendMessage, message)
    
    def is_authed(self, environ):
        return False #TODO
