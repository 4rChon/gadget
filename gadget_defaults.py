##general stuff
NICKNAME = "Gadget"
COMMAND_PREFIX = "!"
ADMINISTRATORS = [ #people with access to commands such as !reload
    ("skype name", "irc mask", "steamid"),
]
ROUTING_FILE = "routes.py" #path to python script that specifies message routes
                            #(see routing.py.example for more information)

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

AUTH_FAILURE_MESSAGES = [
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
]
PLS_MESSAGES = [
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
NAME_MESSAGES = [ #what to say when people say the bot's name
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

##misc

UNICODE_BLACKLIST = [
    '\u202e', #right-to-left control character (thanks, goppend)
]
