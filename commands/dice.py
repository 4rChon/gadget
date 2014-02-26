#!/usr/bin/env python
import sys
import random

try:
    if len(sys.argv) == 2:
        min = 1
        max = int(sys.argv[1])
    elif len(sys.argv) == 3:
        min = int(sys.argv[1])
        max = int(sys.argv[2])
    else:
        min = 1
        max = 20
    
    assert min < max
except ValueError:
    print "I know that's not a number, you know that's not a number. Stop being a dingus, ya dingus."
    
    raise SystemExit
except AssertionError:
    print "Didn't you learn how to math? %d is not less than %d" % (min, max)
    
    raise SystemExit

print random.randrange(1, max+1)
