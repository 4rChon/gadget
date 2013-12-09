#general stuff
NICKNAME = "Gadget"
COMMAND_PREFIX = "!"
ADMINISTRATORS = [ #people with access to commands such as !reload
    ("skype name", "irc mask", "steamid"),
]

#connection information
#blank hosts disable those servers
IRC_HOST = "localhost:6667"
IRC_CHANNEL = "#channel"

GLOBALCHAT_HOST = "localhost:5432"

#servers hosted by the bot
ECHOER_HOST = "0.0.0.0:2345"

#for debugging
MANHOLE_HOST = ""
MANHOLE_PASSWORD = ""

#messages
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

SUS_MARKERS = ["sus"]
SUS_TRANSLATIONS = {
    "goppend": ["gopsus", "hi goppend", "heil goppend"],
}
