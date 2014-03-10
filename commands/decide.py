#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import random

random.seed(time.time())


if random.choice([True, False]):
    print "yes"
else:
    if random.choice([True, False]):
        print "only on tuesdays"
    else:
        print "no"

