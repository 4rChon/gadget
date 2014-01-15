#!/usr/bin/env python
import os
import sys
import random
import time

random.seed(time.time())

who = None

if len(sys.argv) > 1:
    who = " ".join(sys.argv[1:])

if not who:
    who = os.environ["NAME"]

msg = "sus %s" % (who,)

for x in range(0, 5):
    print (" "*random.randrange(0, 15)) + msg

