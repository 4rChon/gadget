#!/usr/bin/env python2
import sys
import string
import random

chars = string.letters + string.punctuation

sys.stdout.write(random.choice(string.letters)) #no slashes plz

if len(sys.argv) > 1:
    try:
        if len(sys.argv) > 2:
            min = int(sys.argv[1])
            max = int(sys.argv[2])
        else:
            min = 10
            max = int(sys.argv[1])
        
        assert min < max
    except:
        print "you're a huge dingus\njust thought you should know"
        
        raise SystemExit
else:
    min = 10
    max = 35

for x in range(0, random.randint(min, max+1)):
    sys.stdout.write(random.choice(chars))

print

