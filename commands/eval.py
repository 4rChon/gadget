#!/usr/bin/env python
from __future__ import print_function
import sys

#useful stuff
import math, random, time, struct

class TimeWrapper(object):
    accept2dyear = time.accept2dyear
    altzone = time.altzone
    asctime = time.asctime
    clock = time.clock
    ctime = time.ctime
    daylight = time.daylight
    gmtime = time.gmtime
    localtime = time.localtime
    mktime = time.mktime
    strftime = time.strftime
    strptime = time.strptime
    struct_time = time.struct_time
    time = time.time
    
    @staticmethod
    def sleep(*args):
        print("fku jon")
        
        raise SystemExit

args = " ".join(sys.argv[1:])
printMode = True
environ = {
    "__builtins__": None,
    "math": math,
    "random": random,
    "time": TimeWrapper,
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

if type(result) is unicode:
    result = result.encode("utf-8")

if type(result) is str:
    result = result.split("\n")
    
    for index, line in enumerate(result):
        while line.startswith("/"):
            line = line[1:]
        
        result[index] = line
    
    while "" in result:
        result.remove("")
    
    result = "\n".join(result)

if printMode:
    print (result)

