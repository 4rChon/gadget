import imp
import traceback
from functools import wraps

from twisted.internet import reactor

from gadget import get_setting
from gadget.globals import Globals

_duplexes = []
_globals = None
_routes = None
_subscribers = []

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
        return "<Address %s_%s at %s>" % (self.protocol, self.address, hex(id(self)))
    
    def __hash__(self):
        return hash((self.protocol, self.address))
    
    def __eq__(self, other):
        if type(other) != type(self):
            return False
        
        return (self.protocol == other.protocol) and (self.address == other.address)

def subscribe(func):
    """Register func to receive incoming messages."""
    
    _subscribers.append(func)

def get_destinations(context):
    """Determine where the given message is supposed to go."""
    
    protocolName = context.get("protocol").PROTOCOL_NAME
    source = Address(protocolName, context.get("source"))
    result = {}
    
    if source in _globals:
        for dest in _globals:
            if dest == source:
                continue
            
            result[dest.protocol] = result.get(dest.protocol, []) + [dest]
    else:
        for dest in _routes.get(protocolName).get(source, []):
            result[dest.protocol] = result.get(dest.protocol, []) + [dest]
    
    context.get("destination").update(result)

def send_message(context):
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

def send_global(body):
    """Sends a message to all global channels."""
    
    context = {}
    
    context.update({"body": body,
                    "protocol": None,
                    "isFormatted": True})
    
    for destination in _globals:
        context.update({"destination": destination.address})
        Globals.protocols.get(destination.protocol).send_message(context)

def handle_message(context):
    """Called by protocols when a message is received."""
    
    try:
        for callback in _subscribers:
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
    result.update({"isEmote": False, #default values for optional entries
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
    
    context["body"] = filter_unicode(context["body"])
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

def duplex(sourceA, sourceB):
    """Create a mapping in the routing table between two sources."""
    
    def callback():
        routes = get_setting("ROUTING_TABLE")
        
        routes.get(sourceA.protocol, {}).get("routes", {}).update({sourceA.address, sourceB})
        routes.get(sourceB.protocol, {}).get("routes", {}).update({sourceB.address, sourceA})
    
    _duplexes.append(callback)

def filter_unicode(str):
    """Removes blacklisted unicode characters, and encodes as UTF-8."""
    
    for char in get_setting("UNICODE_BLACKLIST"):
        str.replace(char, "")
    
    if type(str) is unicode:
        str = str.encode("utf-8")
    
    return str

def load_routes():
    global _routes, _globals
    
    _routes = {}
    _globals = []
    table = get_setting("ROUTING_TABLE", {})
    
    #add duplexes
    for func in _duplexes:
        func()
    
    #process the routing table, compiling a list of global channels and a dict of explicit routes
    for protocolName, data in table.items():
        if Globals.protocols.get(protocolName) == None: #ignore unloaded protocols
            continue
        
        if data.get("globals") != None:
            for destination in data.get("globals"): #convert each global source into an Address object
                _globals.append(Address(protocolName, destination, data.get("globalFormatter")))
        
        if data.get("routes") != None:
            _routes[protocolName] = {}
            
            for source, destinations in data.get("routes").items():
                for destination in destinations:
                    if Globals.protocols.get(destination.protocol) != None:
                        addr = Address(protocolName, source)
                        
                        if addr not in _routes.get(protocolName):
                            _routes.get(protocolName).update({addr: []})
                        
                        _routes.get(protocolName).get(addr).append(destination)

subscribe(lambda context: send_message(context))
