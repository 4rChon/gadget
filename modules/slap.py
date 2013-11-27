#!/usr/bin/env python
import sys

try:
    target = " ".join(sys.argv[1:])
except:
    target = "goppend"

print "/me slaps %s with a halibut" % (target,)

