import imp
import traceback
from functools import wraps

from gadget import get_setting
from gadget.globals import Globals

_routes = None
_subscribers = []
_incomingSubscribers = []

class Address(object):
    """Container for message destination address and related metadata, used in routing table."""
    
    def __init__(self, protocol, address, formatter=None, **kwargs):
        self.dict = {
            "protocol": protocol,
            "address": address,
        }
        
        self.dict.update({"formatter": formatter if formatter else default_format})
        self.dict.update(kwargs)
    
    def __getattr__(self, name):
        return self.dict.get(name, None)
    
    def __repr__(self):
        return "<destination %s_%s at %s>" % (self.protocol, self.address, hex(id(self)))

def subscribe(protocol):
    """Register protocol to receive outgoing global messages."""
    
    _subscribers.append(protocol)

def subscribe_incoming(func):
    """Register func to receive incoming messages."""
    
    _incomingSubscribers.append(func)

def get_destinations(context):
    """Walk the routing table and determine where the given message is supposed to go."""
    
    msgSource = context.get("source")
    result = {}
    globals = {}
    isGlobal = False
    
    def update_list(name, value, dict=globals):
        dict[name] = dict.get(name, []) + [value]
    
    for protocolName, data in _routes.iteritems():
        protocol = Globals.protocols.get(protocolName)
        
        if protocolName == protocol.PROTOCOL_NAME:
            for destination in data.get("globals"):
                if destination.address == msgSource: #determine if the message is global
                    isGlobal = True
                else: #otherwise get this protocol's globals
                    update_list(protocolName, destination)
            
            for source, destinations in data.get("routes").iteritems(): #get destinations for this source
                if source == msgSource:
                    for destination in destinations:
                        update_list(destination.protocol, destination, result)
        else:
            for source in data.get("globals"): #get globals for other protocols
                update_list(protocolName, source)
    
    if isGlobal:
        result.update(globals)
    else:
        context.update({"isGlobal": False})
    
    context.get("destination").update(result)

def send_message(context, exclude=None):
    """Delivers outgoing messages to protocols."""
    
    if len(context.get("destination", {}).keys()) == 0:
        get_destinations(context)
    
    for protocol, destinations in context.get("destination").iteritems():
        protocol = Globals.protocols.get(protocol)
        
        for destination in destinations:
            context = context.copy()
            context["destination"] = destination.address
            
            format(context, destination)
            protocol.send_message(context)

def send_global(body, exclude=None):
    """Sends a message to all subscribed protocols."""
    
    context = {}
    
    context.update({"body": body,
                    "protocol": None,
                    "isGlobal": True,
                    "isFormatted": True})
    send_message(context, exclude)

def handle_message(context):
    """Called by protocols when a message is received."""
    
    try:
        for callback in _incomingSubscribers:
            callback(context.copy())
    except StopIteration:
        pass

def make_context(protocol, source, name, body, **kwargs):
    """Builds a context dictionary."""
    
    result = {}
    
    result.update({"protocol": protocol, #required entries
                   "source": source,
                   "name": name,
                   "body": body})
    result.update({"isGlobal": True, #default values for optional entries
                   "isEmote": False,
                   "isFormatted": False,
                   "destination": {}})
    result.update(kwargs) #everything else
    
    return result

def format(context, destination):
    """Prepare an outgoing message for sending."""
    
    if not context.get("isFormatted"):
        if hasattr(context.get("protocol"), "format_message"):
            context.get("protocol").format_message(context)
        
    if not context.get("isFormatted"):
        destination.formatter(context)
    
    context["isFormatted"] = True

def default_format(context):
    """Performs default formatting of messages."""
    
    res = "[%s] %s: %s" % (context["protocol"].PROTOCOL_NAME,
                           context["name"],
                           context["body"])
    
    context.update({"body": res, "isFormatted": True})

def intraprotocol_formatter(func):
    """Allows a formatting function to return None or False, thus using default_format instead.
       Shortens special formatting functions of intra-protocol global messages."""
    
    @wraps(func)
    def wrapper(context):
        result = func(context)
        
        if not result: #func returned None or False
            default_format(context)
    
    return wrapper

def filter_unicode(str):
    """Removes blacklisted unicode characters, and encodes as UTF-8."""
    
    for char in get_setting("UNICODE_BLACKLIST"):
        str.replace(char, "")
    
    if type(str) is unicode:
        str = str.encode("utf-8")
    
    return str

def load_routes():
    global _routes
    
    _routes = get_setting("ROUTING_TABLE", {})
    
    #preprocess the table so assumtions can be made in get_destinations
    for protocolName, data in _routes.items():
        if Globals.protocols.get(protocolName) == None:
            _routes.pop(protocolName)
            
            continue
        
        if data.get("globals") == None:
            _routes[protocolName]["globals"] = []
        else:
            for index, destination in enumerate(data.get("globals")): #convert each global source into a Address object
                _routes[protocolName]["globals"][index] = Address(protocolName,
                                                                  destination,
                                                                  data.get("globalFormatter"))
        
        if data.get("routes") == None:
            _routes[protocolName]["routes"] = {}
        else:
            for _, destinations in data.get("routes").items():
                for destination in destinations:
                    if Globals.protocols.get(destination.protocol) == None:
                        _routes[protocolName]["routes"].remove(destination)

subscribe_incoming(lambda context: send_message(context))
