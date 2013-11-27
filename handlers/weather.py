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

print (u"{0} {1}°. {2} ({3})".format(data["location"], current["temperature"], " ".join(current["weather"]), current["remark"])).encode("utf-8")
