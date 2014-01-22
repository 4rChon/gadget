from gadgetlib.Globals import Globals

class AuthenticationError(Exception):
    """Rasied by require_auth when the user is not authenticated."""
    
    pass

class WaitingForAuthenticationNotice(Exception):
    """Raised by require_auth when waiting for authentication verification to complete."""
    
    pass

def filter_unicode(str):
    for char in Globals.settings.UNICODE_BLACKLIST:
        str.replace(char, "")
    
    if type(str) is unicode:
        str = str.encode("utf-8")
    
    return str
