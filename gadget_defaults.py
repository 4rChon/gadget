#vim: set ft=python:
#sublime: x_syntax Packages/Python/Python.tmLanguage

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
#MANHOLE_HOST = "0.0.0.0:2345"
#MANHOLE_PASSWORD = "changeme"

#messages
AUTH_FAILURE_MESSAGES = [
    "messages to send when someone is not authorized to run a command",
]
PLS_MESSAGES = [
    "messages to send when someone is fed up with the bot",
]
SUS_TRANSLATIONS = {
    "name to match": ["list", "of", "greetings"],
}
