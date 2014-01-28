from gadget.plugins import make_deferred
from gadget.commands import register_command

def handle_help(self, cmd, args, context):
    """!help [command name]\nShows you help n' stuff."""
    
    if len(args) > 0:
        name = args[0]
        
        try:
            handler = self.handlers[name]
        except KeyError:
            return make_deferred("No such command.")
        
        if handler == self.run_handler:
            return make_deferred("I don't know what {0} does.\ntry !{0} help".format(name))
        else:
            if hasattr(handler, "__doc__") and type(handler.__doc__) is str:
                return make_deferred(handler.__doc__)
            else:
                return make_deferred("I don't know what {0} does.".format(name))
    else:
        return make_deferred("I know about the following commands: " + ", ".join(self.handlers.keys()))

def initialize():
    register_command(handle_help)
