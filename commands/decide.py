#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import random

random.seed(time.time())


if random.choice([True, False]):
    print "yes"
else:
    print "no"

