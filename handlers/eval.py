#!/usr/bin/env python
from __future__ import print_function
import sys

#useful stuff
import math, random, time

args = " ".join(sys.argv[1:])
printMode = True

if args.startswith("_="):
    printMode = False
    args = args[2:]

result = eval(args)

if printMode:
    print (result)

