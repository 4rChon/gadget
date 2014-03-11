#!/usr/bin/env python
import sys
import os
import random
import time

random.seed(time.time())

NOUNS = "data\slap_nouns.txt"
ADJECTIVES = "data\slap_adjectives.txt"

slapMsgs = [
    "slaps {0} around a bit with a {1} {2}.",
    "runs {0} over with a {1} {2}.",
    "drives {0} over a {1} {2}.",
    "pokes {0} with a {1} rod of {2}.",
    "touches {0} with a piece of {1} {2}.",
    "revokes {0}'s {1} {2}.",
    "persuades {0} with a {1} {2}.",
    "types \"rm -rf /\" on {0}'s {1} {2}.",
    "eats {0}'s every single {1} {2}.",
    "finds {0}'s picture in the dictionary, next to the definition of \"{1} {2}.\"",
    "seduces {0} with a {1} {2}",
    "touches {0} inappropriately with a {1} {2}",
]

def add_adjective(word):
    with open(ADJECTIVES, "a") as f:
        f.write(word + "\n")
        
    print ("{} added to adjectives.".format(word))
    
def add_noun(word):
    with open(NOUNS, "a") as f:
        f.write(word + "\n")
    
    print ("{} added to nouns.".format(word))
    
def add_word(wordType, word):
    if wordType == "adjective":
        add_adjective(word)
    elif wordType == "noun":
        add_noun(word)

def list_adjectives():
    try:
        with open(ADJECTIVES, "r") as f:
            print ", ".join(f.read().split("\n"))
    except IOError:
        print("{} not found").format(ADJECTIVES)
        
def list_nouns():
    try:
        with open(NOUNS, "r") as f:
            print ", ".join(f.read().split("\n"))
    except IOError:
        print("{} not found").format(NOUNS)
        
def list_type(wordType):
    if wordType == "adjective":
        list_adjectives()
    if wordType == "noun":
        list_noun()

def list_all():
    print("Adjectives: ")
    list_adjectives()
    print("Nouns: ")
    list_nouns()

def get_adjectives():
    try:
        with open(ADJECTIVES, "r") as f:
            adjectives = f.read().split("\n")
    except IOError:
        adjectives = []
        
    return adjectives
        
def get_nouns():
    try:
        with open(NOUNS, "r") as f:
            nouns = f.read().split("\n")
    except IOError:
        nouns = []
        
    return nouns
    
def get():

    adjectives = get_adjectives()
    nouns = get_nouns()
        
    while "" in adjectives:
        adjectives.remove("")
        
    while "" in nouns:
        nouns.remove("")
        
    if len(nouns) < 1:
        print "I don't have any objects to slap with"
        
        raise SystemExit
        
    adjective = random.choice(adjectives)
    noun = random.choice(nouns)
    
    try:
        target = sys.argv[1]
    except:
        target = os.environ.get("name", "goppend")
    
    print ("/me %s" % (random.choice(slapMsgs),)).format(target, adjective, noun)

if len(sys.argv) > 1:
    getcmd = sys.argv[1].lower()
    
    if getcmd == "list":
        if len(sys.argv) > 2:
            wordType = sys.argv[2]
            if wordType in ["adjective", "noun"]:
                list_type(wordType)
            else:
                print("You pick your nose with those fingers?")
        else:
            list_all()
    elif getcmd == "add":
        if len(sys.argv) > 3:
            wordType = sys.argv[2]
            if wordType in ["adjective", "noun"]:
                add_word(wordType, (" ".join(sys.argv[3:])))
            else:
                print("How high are you on a scale of rusty cliffs to jizz stained chair legs?")
        else :
            print("Pass me some of what you're smoking bro")
    else:
        get()
else:
    print("Who do you want me to slap?")

