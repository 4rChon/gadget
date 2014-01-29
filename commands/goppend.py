#!/usr/bin/env python
import urllib2
import random
import re

regex = re.compile(r".*?\"(.*?)\" - goppend")

def get_quotes():
    request = urllib2.urlopen("http://labs.beniesbuilds.com/python/qotd/?action=search&q=goppend&format=raw")
    
    return request.read().split("\n")

def choose_quote():
    quotes = get_quotes()
    
    while True:
        yield random.choice(quotes)

def main():
    quotes = choose_quote()
    match = None
    
    while not match:
        match = regex.match(quotes.next())
    
    print match.groups()[0]

if __name__ == '__main__':
    main()
