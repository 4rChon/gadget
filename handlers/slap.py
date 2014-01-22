#!/usr/bin/env python
import sys
import os
import random
import time

random.seed(time.time())

slapMsgs = [
    "slaps {0} around a bit with a large trout.",
    "runs {0} over with a bulldozer.",
    "drives {0} over a cliff.",
    "pokes {0} with a glowing-hot rod of steel.",
    "touches {0} with a piece of moldy bread.",
    "revokes {0}'s internet access.",
    "persuades {0} with a longsword.",
    "types \"rm -rf /\" on {0}'s terminal.",
    "eats all of {0}'s cookies.",
    "finds {0}'s picture in the dictionary, next to the definition of \"stupid.\"",
    "seduces {0} with a grill",
    "touches {0} inappropriately with a chair leg",
]

try:
    target = sys.argv[1] or os.environ["name"]
except:
    target = os.environ["name"]

print ("/me %s" % (random.choice(slapMsgs),)).format(target)

