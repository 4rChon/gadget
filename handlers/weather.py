#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

import thefuckingweather

try:
    target = " ".join(sys.argv[1:])
except:
    target = ""

try:
    data = thefuckingweather.get_weather(target)
    current = data["current"]
except thefuckingweather.LocationError:
    print "I CAN'T FIND THAT SHIT"
    
    raise SystemExit

if len(sys.argv) < 2:
    print (u"{3}: {1} ({0}°) ({2})".format(current["temperature"], " ".join(current["weather"]), current["remark"], data["location"])).encode("utf-8")
else:
    print (u"{1} ({0}°) ({2})".format(current["temperature"], " ".join(current["weather"]), current["remark"])).encode("utf-8")
