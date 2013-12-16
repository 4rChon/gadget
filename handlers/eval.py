#!/usr/bin/env python
from __future__ import print_function
import sys

#useful stuff
import math, random, time, struct

args = " ".join(sys.argv[1:])
printMode = True
environ = {
    "__builtins__": None,
    "math": math,
    "random": random,
    "time": time,
    "struct": struct,
    "print": print,
    "range": xrange,
    "dir": dir,
    "len": len,
    "all": all,
    "any": any,
    "reversed": reversed,
    "chr": chr,
    "ord": ord,
    "int": int,
    "float": float,
    "long": long,
    "str": str,
    "bin": bin,
    "hex": hex,
    "sum": sum,
}

if args.startswith("_="):
    printMode = False
    args = args[2:]

result = eval(args, environ, environ)

if printMode:
    print (result)

