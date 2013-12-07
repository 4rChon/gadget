#!/usr/bin/env python
import sys
import os
import random

PATH = "data/centipede.txt"

def add(word):
    with open(PATH, "a") as f:
        f.write(word + "\n")
    
    print word

def get():
    try:
        with open(PATH, "r") as f:
            words = f.read().split("\n")
    except IOError:
        words = []
    
    while "" in words:
        words.remove("")
    
    if len(words) < 1:
        print "I don't have enough data to centipede"
        
        raise SystemExit
    
    word = random.choice(words)
    
    if random.randint(0, 1):
        word += "!"
    
    print word

if len(sys.argv) > 1:
    if sys.argv[1].lower() == "add" and len(sys.argv) > 2:
        add(" ".join(sys.argv[2:]))
    else:
        print "I will not %s" % (sys.argv[1],)
else:
    get()
