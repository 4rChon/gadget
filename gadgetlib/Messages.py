from gadgetlib import filter_unicode

_subscribers = []
_incomingSubscribers = []

def subscribe(protocol):
    """Register protocol to receive outgoing global messages."""
    
    _subscribers.append(protocol)

def subscribe_incoming(func):
    """Register func to receive incoming messages."""
    
    _incomingSubscribers.append(func)

def send_message(context):
    if type(context) is str:
        context = {"body": context, "name": "Gadget", "protocol": None}
    
    for protocol in _subscribers:
        if protocol != context["protocol"]:
            protocol.send_message(context)

def handle_message(context):
    try:
        for callback in _incomingSubscribers:
            context = callback(context) or context
    except StopIteration:
        pass

def make_context(protocol, source, name, body, **kwargs):
    result = {}
    
    result.update({"protocol": protocol,
                   "source": source,
                   "name": filter_unicode(name),
                   "body": filter_unicode(body)})
    result.update({"isGlobal": True,
                   "isEmote": False})
    result.update(kwargs)
    
    return result

def _send_global(context):
    if context.get("isGlobal"):
        send_message(context)

subscribe_incoming(_send_global)
