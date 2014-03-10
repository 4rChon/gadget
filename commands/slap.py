#!/usr/bin/env python
import sys
import os
import random
import time

random.seed(time.time())

slapNouns = [
    "chair leg",
    "cliff",
    "trout",
    "steel",
    "internet access",
    "longsword",
    "terminal",
    "cookie",
    "grill",
]
    
slapAdjectives = [
    "large",
    "glowing-hot",
    "rusty",
    "moldy",
    "red",
    "old",
    "brand spanking new",
    "jizz stained",
    "stupid",
]

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

try:
    target = sys.argv[1]
except:
    target = os.environ.get("name", "goppend")

print ("/me %s" % (random.choice(slapMsgs),)).format(target, random.choice(slapAdjectives), random.choice(slapNouns))

