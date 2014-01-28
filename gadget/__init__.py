from gadget.Globals import Globals

class AuthenticationError(Exception):
    """Rasied by require_auth when the user is not authenticated."""
    
    pass

class WaitingForAuthenticationNotice(Exception):
    """Raised by require_auth when waiting for authentication verification to complete."""
    
    pass
