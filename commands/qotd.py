#!/usr/bin/env python
import sys
import urllib, urllib2

def fetch(action, url="http://labs.beniesbuilds.com/python/qotd/?format=raw"):
    try:
        return urllib2.urlopen(url + "&action=" + action).read()
    except urllib2.HTTPError as e:
        return "Error: HTTP %d" % e.code

if len(sys.argv) < 2:
    print fetch("")
else:
    cmd = sys.argv[1].lower()
    
    if   cmd == "random":
        print fetch("random")
    elif cmd == "latest":
        print fetch("latest")
    elif cmd == "search":
        query = urllib.urlencode({"q": " ".join(sys.argv[2:])})
        print fetch("search&" + query)
    else:
        try:
            id = int(cmd)
            
            print fetch("&id=%d" % (id,))
        except ValueError:
            print "I don't know how to %s" % (cmd,)

