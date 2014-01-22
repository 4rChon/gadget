from gadgetlib.Globals import Globals

_subscribers = []
_incomingSubscribers = []

def subscribe(protocol):
    """Register protocol to receive outgoing global messages."""
    
    _subscribers.append(protocol)

def subscribe_incoming(func):
    """Register func to receive incoming messages."""
    
    _incomingSubscribers.append(func)

def send_message(context, exclude=None):
    """Delivers outgoing messages to protocols."""
    
    for protocol in _subscribers:
        if protocol == exclude:
            continue
        
        tmpContext = context.copy()
        
        if not context.get("isFormatted"):
            try:
                format = getattr(protocol, "format_message")
            except AttributeError:
                format = default_format
            
            tmpContext = format(context)
        
        tmpContext.update({"source": None})
        
        protocol.send_message(tmpContext)

def send_global(body):
    """Sends a message to all subscribed protocols."""
    
    context = {}
    
    context.update({"body": body,
                    "protocol": None,
                    "isGlobal": True,
                    "isFormatted": True})
    send_message(context)

def handle_message(context):
    """Called by protocols when a message is received."""
    
    try:
        for callback in _incomingSubscribers:
            context = callback(context) or context
    except StopIteration:
        pass

def make_context(protocol, source, name, body, **kwargs):
    """Builds a context dictionary."""
    
    result = {}
    
    result.update({"protocol": protocol,
                   "source": source,
                   "name": name,
                   "body": body})
    result.update({"isGlobal": True,
                   "isEmote": False,
                   "isFormatted": False})
    result.update(kwargs)
    
    return result

def default_format(context):
    """Performs default formatting of messages."""
    
    res = filter_unicode("[%s] %s: %s" % (context["protocol"].__class__.__name__,
                                          context["name"],
                                          context["body"]))
    
    context.update({"body": res, "isFormatted": True})
    
    return context

#local functions
def filter_unicode(str):
    for char in Globals.settings.UNICODE_BLACKLIST:
        str.replace(char, "")
    
    if type(str) is unicode:
        str = str.encode("utf-8")
    
    return str

def send_all_msgs(context):
    if context.get("isGlobal"):
        send_message(context, exclude=context.get("protocol"))

subscribe_incoming(send_all_msgs)
