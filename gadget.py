import pdb
import time
import subprocess
import os
import sys
import glob

import Skype4Py as skype4py

ADMINISTRATOR_NAME = "mr.angry"

running = True
restart = False

class Bot(object):
    def __init__(self):
        self.handlers = {}
        self.skype = skype4py.Skype(Transport='x11')
        self.skype.FriendlyName = "Gadget"
        
        self.skype.Attach()
        self.init_handlers()
        
        self.skype.OnMessageStatus = self.message_handler
    
    def init_handlers(self):
        for member in dir(self):
            if member.startswith("handle_"):
                self.handlers.update({member.split("handle_")[1]: getattr(self, member)})
        
        fileCmds = [x.split("/")[1].split(".py")[0] for x in glob.glob("handlers/*.py")]
        
        for file in fileCmds:
            self.handlers.update({file: self.run_handler})
    
    def message_handler(self, msg, status):
        if status == skype4py.cmsReceived:
            if msg.Body.startswith("!"):
                args = msg.Body.split(" ")
                cmd = args[0][1:].lower()
                environ = os.environ.copy()
                environ["SKYPE_NAME"] = msg.FromDisplayName
                environ["SKYPE_HANDLE"] = msg.FromHandle
                
                try:
                    result = self.handlers[cmd](cmd, args[1:], environ)
                except KeyError:
                    result = "No such command"
                
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
        """!help [command name]\nShows you help n' stuff."""
        
        print self.handlers.keys()
        
        if len(args) > 0:
            query = args[0]
            name = "handle_%s" % (query,)
            
            if hasattr(self, name):
                docs = getattr(self, name).__doc__
                
                if docs:
                    return docs
                else:
                    return "I don't know what %s does" % (query,)
            elif query in self.handlers.keys():
                return "I don't know what %s does\nTry !%s help" % (query, query)
            else:
                return "No such command"
        
        return "I know about the following commands: " + ", ".join(self.handlers.keys())
    
    def handle_reload(self, cmd, args, environ):
        global running, restart
        
        if not environ["SKYPE_HANDLE"] == ADMINISTRATOR_NAME:
            return "You are unauthorized!"
        
        running = False
        restart = True
    
if __name__ == "__main__":
    bot = Bot()
    
    while running:
        time.sleep(1)
    
    if restart:
        sys.argv[0] = os.path.abspath(sys.argv[0])
        
        os.execv("/usr/bin/env", ["env", "python"] + sys.argv)
