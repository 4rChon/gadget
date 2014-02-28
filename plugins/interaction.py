import random
import re

from gadget import get_setting
from gadget.messages import subscribe, send_message, get_response_context

def reply(context, body):
    context = get_response_context(context)
    context["body"] = body
    
    send_message(context)

def scan_name(context):
    if re.match(get_setting("NAME_REGEX") % (get_setting("NICKNAME"),), context["body"], re.I):
        reply(context, random.choice(get_setting("NAME_MESSAGES")))

def scan_pls(context):
    if re.match(get_setting("PLS_REGEX") % (get_setting("NICKNAME"),), context["body"], re.I):
        reply(context, random.choice(get_setting("PLS_MESSAGES")))

def initialize():
    subscribe(scan_name)
    subscribe(scan_pls)
