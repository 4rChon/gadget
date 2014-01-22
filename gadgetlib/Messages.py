from gadgetlib import filter_unicode

_subscribers = []
_incomingSubscribers = []

def subscribe(protocol):
    """Register protocol to receive outgoing global messages."""
    
    _subscribers.append(protocol)

def subscribe_incoming(func):
    """Register func to receive incoming messages."""
    
    _incomingSubscribers.append(func)

def default_format(context):
    res = filter_unicode("[%s] %s: %s" % (context["protocol"].__class__.__name__,
                                          context["name"],
                                          context["body"]))
    
    context.update({"body": res, "isFormatted": True})
    
    return context

def send_message(context, exclude=None):
    for protocol in _subscribers:
        if protocol == exclude:
            continue
        
        tmpContext = context.copy()
        
        if not context["isFormatted"]:
            format = getattr(protocol, "format_message") or default_format
            tmpContext = format(context)
        
        protocol.send_message(tmpContext)

def send_global(body):
    context = {}
    
    context.update({"body": body,
                   "protocol": None,
                   "isGlobal": True,
                   "isFormatted": True})
    send_message(context)

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
                   "isEmote": False,
                   "isFormatted": False})
    result.update(kwargs)
    
    return result

def send_all_msgs(context):
    if context.get("isGlobal"):
        send_message(context, exclude=context.get("protocol"))

subscribe_incoming(send_all_msgs)
