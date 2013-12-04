#!/usr/bin/env python2
import sys
import string
import random

chars = string.letters + string.punctuation

for x in range(0, random.randint(10, 35)):
    sys.stdout.write(random.choice(chars))

print

