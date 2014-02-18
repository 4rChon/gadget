import random

from gadget import get_setting
from gadget.messages import subscribe_incoming, send_message

def translate_sus(name):
    for k,v in get_setting("SUS_TRANSLATIONS").iteritems():
        if "," in k:
            k = k.split(",")
            
            if any([test in name for test in k]):
                return random.choice(v)
        else:
            if k in name:
                return random.choice(v)
    
    return "sus %s" % (name,)

def scan(context):
    name = context.get("name")
    body = context.get("body")
    
    if body in get_setting("SUS_MARKERS"):
        tmp = context.copy()
        tmp["body"] = translate_sus(name)
        tmp["isFormatted"] = True
        
        send_message(tmp)

def initialize():
    subscribe_incoming(scan)
