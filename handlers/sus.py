#!/usr/bin/env python
import os
import sys
import random
import time

random.seed(time.time())

word = "sus"
who = None

if len(sys.argv) > 1:
    if any([sys.argv[1].startswith(x) for x in ['"', "'"]]):
        word = sys.argv[1][1:][:-1]
        
        sys.argv.pop(1)
    
    if len(sys.argv) >1:
        who = " ".join(sys.argv[1:])

if not who:
    who = os.environ["NAME"]

msg = "%s %s" % (word, who,)

for x in range(0, 5):
    print (" "*random.randrange(0, 15)) + msg

