"""
Set the topic globally.

Addresses must be explicitly configured to receive the new topic in routes.py like so:
    Address("Protocol", "address", receiveTopic=True, topicCommand="/topic %s")
where %s is replaced with the new topic.
"""
from gadget import get_setting
from gadget.plugins import require_auth
from gadget.commands import register_command
from gadget.messages import _globals, _routes, send_message
from gadget.globals import Globals

def get_destinations():
    for dest in _globals:
        yield dest
    
    for dests in _routes.values():
        for dest in dests:
            yield dest

def send_to_destination(addr, body):
    context = {
        "protocol": Globals.protocols.get(addr.protocol),
        "destination": {addr.protocol: [addr]},
        "body": body,
        "isFormatted": True,
    }
    
    send_message(context)

@require_auth
def handle_topic(self, cmd, args, context):
    """!topic [new topic]\nThe [new topic] Tavern"""
    
    for dest in get_destinations():
        if dest.receiveTopic:
            command = dest.topicCommand or "/topic %s"
            newTopic = get_setting("TOPIC_FORMAT", "%s") % (" ".join(args),)
            msg = command % (newTopic,)
            
            send_to_destination(dest, msg)

def initialize():
    register_command(handle_topic)
