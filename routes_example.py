from gadget.messages import Address, simple_formatter, duplex #useful imports

@simple_formatter #decorator that uses default_format if we don't tell it to do otherwise
def irc_formatter(context):
    if context["protocol"].PROTOCOL_NAME == "IRC":
        context["body"] = "<#%s> %s: %s" % (context.get("source").split("#")[1], #do the formatting
                                            context.get("name"),
                                            context.get("body"))
        
        return True #tell the decorator we've done the formatting

def bridge_formatter(context): #another formatter
    context["body"] = "%s: %s" % (context.get("name"), context.get("body"))

GLOBAL_CHANNELS = [ #messages received by any of these channels are sent to every other channel
                    #with optional formatting
    Address("IRC", "localhost:6667#channel", irc_formatter),
    Address("IRC", "localhost:6667#otherchannel", irc_formatter),
    Address("Skype", "#echo123/$d5740b91fb44464c"),
]

ROUTES = {
    Address("IRC": "localhost:6667#bridge"): [ #if a message comes from here
        Address("Skype", "#echo123/$ed1d190e410d152a", bridge_formatter), #send it to these channels
    ],
    Address("Skype", "#echo123/$ed1d190e410d152a"): [ #formatter argument is ignored here
        Address("IRC": "localhost:6667#bridge", bridge_formatter), #but used here
                                                                   #you can also pass named arguments
                                                                   #certain plugins may use this additional data (e.g. topic)
    ],
}

#this is a shorter way to express the above routing table
#each channel's messages are routed to the other
duplex(Address("IRC", "localhost:6667#bridge", bridge_formatter),
       Address("Skype", "#echo123/$ed1d190e410d152a", bridge_formatter))
