#!/usr/bin/env python
import sys

item = "propane"

if len(sys.argv) > 1:
    item = " ".join(sys.argv[1:])

print "I sell {0} and {0} accessories.".format(item)
