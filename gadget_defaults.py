##general stuff
NICKNAME = "Gadget"
COMMAND_PREFIX = "!"
ADMINISTRATORS = [ #people with access to commands such as !reload
    ("skype name", "irc mask", "steamid"),
]

try:
    from routes import GLOBAL_CHANNELS, ROUTES
except Exception as e:
    print "Warning: unable to import message routing data (%s: %s)" % (e.__class__.__name__, str(e),)
    
    GLOBAL_CHANNELS = []
    ROUTES = {}

COMMAND_PATHS = ["commands"] #paths to folders with command scripts
PLUGIN_PATHS = ["plugins"] #paths to folders with additional plugin modules
PROTOCOL_PATHS = ["protocols"] #paths to folders with additional protocol modules

##connection information
##a blank address disables the server

IRC_CONNECTIONS = {"localhost:6667": ["#channel"]} #dict of networks to connect to, and channels to join on each

GLOBALCHAT_ADDRESS = ""

TWITCH_USERNAME = ""
TWITCH_OATH_TOKEN = "" #visit http://twitchapps.com/tmi/ to generate this
TWITCH_CHANNELS = [] #list of channel names to join

#ECHOER_BIND_ADDRESS = "0.0.0.0:2345" #sends incoming datagrams as messages

#interpreter over ssh, for debugging
#MANHOLE_BIND_ADDRESS = ""
#MANHOLE_PASSWORD = ""

##messages
AUTH_FAILURE_MESSAGES = [ #let that dingus know they ain't nobody we listen to
    "I am a strong black woman who don't need no man",
    "no",
    "lol",
    "ok, I'll get right on that",
    "how about no?",
    "maybe tomorrow",
    "I don't like your face, so no",
    "no soap, honkie lips.",
    "you silly, twisted boy you.",
    "just what do you think you're doing, dave?",
    "are you on drugs?",
    "have a gorilla",
    "what, what, what, what, what, what, what, what?",
    "that's something I cannot allow to happen",
    "you can't get the wood, you know",
    "this mission is too important for me to allow you to jeopardize it",
    "get your damn hands off my synthesizer",
    "not without my chapstick",
    "failed attempts to enter her underwater fortress",
    "set yourself on fire",
    "we come in pieces",
    "wherever you go, there you are",
    "papers, please",
]
PLS_REGEX = r"%s(,|\.+|!+)? +(pls|plz|please|why)" #%s is replaced with nickname
PLS_MESSAGES = [ #what to say when people are dissatisfied with the behaviour of the bot
    "NO!",
    "it wasn't me",
    "shitty programming?",
    "this is all Yop's fault, I swear!",
    "oops",
    "pls urself",
    "no!",
    "nyet",
    "nein",
]
NAME_REGEX = r"((hi|hello|sus|greetings|yo|hey|sup) +)?%s$" #%s is replaced with nickname
NAME_MESSAGES = [ #what to say when people address the bot
    "sus",
    "beep",
    "boop",
    "beepboop"
    "bzzrt",
    "greetings",
    "hi",
    "yes?",
    "yes, this is gadget"
]

SUS_MARKERS = ["sus", "hi"] #when somebody sends a message consisting only of these strings
SUS_TRANSLATIONS = { #greet them in a special way
    "goppend": ["gopsus", "hi goppend", "heil goppend"],
}

TOPIC_FORMAT = "%s" #format for a topic set by !topic, %s is replaced with the command's arguments

##misc
UNICODE_BLACKLIST = [
    '\u202e', #right-to-left control character (thanks, goppend)
]
