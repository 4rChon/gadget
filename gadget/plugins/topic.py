from gadget.plugins import require_auth
from gadget.commands import register_command

@require_auth
def handle_topic(self, cmd, args, context):
    """!topic [new topic]\nThe [new topic] Tavern"""
    
    self.send_message("/topic The %s Tavern" % (" ".join(args),))

def initialize():
    register_command(handle_topic)
