import random

from gadget.globals import Globals
from gadget.messages import subscribe_incoming, send_message

def translate_sus(name):
    for k,v in Globals.settings.SUS_TRANSLATIONS.iteritems():
        if type(k) is str:
            if k in name:
                return random.choice(v)
        elif type(k) is list:
            if any([test in name for test in k]):
                return random.choice(v)
    
    return "sus %s" % (name,)

def scan(context):
    name = context.get("name")
    body = context.get("body")
    
    if body in Globals.settings.SUS_MARKERS:
        tmp = context.copy()
        tmp["body"] = translate_sus(name)
        tmp["isFormatted"] = True
        
        send_message(tmp)

def initialize():
    subscribe_incoming(scan)
