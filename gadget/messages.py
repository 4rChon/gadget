import imp
import traceback
from functools import wraps

from gadget import get_setting
from gadget.globals import Globals

_routes = None
_subscribers = []
_incomingSubscribers = []

class Destination(object):
    """Container for destination and formatter, used in routing table."""
    
    def __init__(self, protocol, address, formatter=None):
        self.protocol = protocol
        self.address = address
        
        if not formatter:
            self.formatter = default_format
        else:
            self.formatter = formatter
    
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
    
    for protocolName, data in _routes.iteritems():
        protocol = Globals.protocols.get(protocolName)
        
        if protocolName == protocol.PROTOCOL_NAME:
            for destination in data.get("globals"): #determine if the message is global
                if destination.address == msgSource:
                    isGlobal = True
                else:
                    globals[protocolName] = globals.get(protocolName, []) + [destination]
            
            for source, destinations in data.get("routes").iteritems(): #get destinations for this source
                if source == msgSource:
                    for destination in destinations:
                        if destination.formatter == None:
                            destination.formatter = default_format
                        
                        result[destination.protocol] = result.get(destination.protocol, []) + [destination]
        else: #get globals for other protocols
            for source in data.get("globals"):
                
                globals[protocolName] = globals.get(protocolName, []) + [source]
    
    if isGlobal:
        result.update(globals)
        context.update({"isGlobal": True})
    else:
        context.update({"isGlobal": False})
    
    context.get("destination").update(result)
    
    return context

def send_message(context, exclude=None):
    """Delivers outgoing messages to protocols."""
    
    if len(context.get("destination", {}).keys()) == 0:
        context = get_destinations(context)
    
    for protocol, destinations in context.get("destination").iteritems():
        protocol = Globals.protocols.get(protocol)
        
        for destination in destinations:
            context = context.copy()
            context["destination"] = destination.address
            
            if hasattr(protocol, "format_message"):
                protocol.format_message(context)
            
            if not context.get("isFormatted"):
                destination.formatter(context)
                
                context["isFormatted"] = True
            
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

def default_format(context):
    """Performs default formatting of messages."""
    
    res = "[%s] %s: %s" % (context["protocol"].PROTOCOL_NAME,
                           context["name"],
                           context["body"])
    
    context.update({"body": res, "isFormatted": True})
    
    return context

def intraprotocol_formatter(func):
    """Allows a formatting function to return None, using default_format instead.
       Shortens special formatting functions of intra-protocol global messages."""
    
    @wraps(func)
    def wrapper(context):
        result = func(context)
        
        if not result:
            return default_format(context)
        
        return result
    
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
    
    file = get_setting("ROUTING_FILE", None)
    
    if file:
        try:
            module = imp.load_source("routes", file)
            _routes = module.routingTable
        except IOError:
            print "Warning: routes file %s doesn't exist" % (file,)
        except Exception:
            print "Exception raised when importing routing file:"
            
            traceback.print_exc()
        
        #preprocess the table so assumtions can be made in get_destinations
        for protocolName, data in _routes.items():
            if Globals.protocols.get(protocolName) == None:
                _routes.pop(protocolName)
                
                continue
            
            if data.get("globals") == None:
                _routes[protocolName]["globals"] = []
            else:
                for index, destination in enumerate(data.get("globals")): #convert each global source into a Destination object
                    _routes[protocolName]["globals"][index] = Destination(protocolName,
                                                                          destination,
                                                                          data.get("globalFormatter"))
            
            if data.get("routes") == None:
                _routes[protocolName]["routes"] = {}
            else:
                for _, destinations in data.get("routes").items():
                    for destination in destinations:
                        if Globals.protocols.get(destination.protocol) == None:
                            _routes[protocolName]["routes"].remove(destination)

def _send_all_msgs(context):
    send_message(context)

subscribe_incoming(_send_all_msgs)
