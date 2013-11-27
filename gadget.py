import pdb
import time
import subprocess
import os
import glob
from collections import defaultdict

import Skype4Py as skype4py

ADMINISTRATOR_NAME = "mr.angry"

class Bot(object):
    def __init__(self):
        self.handlers = defaultdict(lambda: self.run_handler)
        self.skype = skype4py.Skype(Transport='x11')
        self.skype.FriendlyName = "Gadget"
        
        self.skype.Attach()
        self.init_handlers()
        
        self.skype.OnMessageStatus = self.message_handler
    
    def init_handlers(self):
        for member in dir(self):
            if member.startswith("handle_"):
                self.handlers.update({member.split("handle_")[1]: getattr(self, member)})
    
    def message_handler(self, msg, status):
        if status == skype4py.cmsReceived:
            if msg.Body.startswith("!"):
                args = msg.Body.split(" ")
                cmd = args[0][1:]
                environ = os.environ.copy()
                environ["SKYPE_NAME"] = msg.FromDisplayName
                environ["SKYPE_HANDLE"] = msg.FromHandle
                result = self.handlers[cmd](cmd, args[1:], environ)
                
                if result:
                    msg.Chat.SendMessage(result)
    
    def run_handler(self, cmd, args, environ):
        if not os.path.exists("handlers/%s.py" % (cmd,)):
            return "Don't know how to %s" % (cmd,)
        
        proc = subprocess.Popen(("python handlers/%s.py %s" % (cmd, " ".join(args))).split(" "),
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                env=environ)
        
        return proc.stdout.read() + proc.stderr.read()
    
    def handle_help(self, cmd, args, environ):
        print args
        
        fileCmds = [x.split("/")[1].split(".py")[0] for x in glob.glob("handlers/*.py")]
        
        return "I know about the following commands: " + ", ".join(self.handlers.keys() + fileCmds)
    
    def handle_reload(self, cmd, args, environ):
        if not environ["SKYPE_HANDLE"] == ADMINISTRATOR_NAME:
            return "You are unauthorized!"
        
        print "exit requested"
        
        raise SystemExit(0)
    
if __name__ == "__main__":
    bot = Bot()
    
    try:
        while True:
            time.sleep(1)
    except SystemExit as e:
        print e
        print e.code
