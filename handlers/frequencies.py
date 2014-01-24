#!/usr/bin/env python
import sys
import random

randrange = (lambda min, max: random.randrange(min, max+1))

def format_frequencies(string):
    times = string.count("%d")
    fmt = ()
    
    for x in range(times):
        fmt += (randrange(0, 9),)
    
    return (string % fmt).strip("0")

def generate_frequencies(count):
    frequencies = []
    
    for x in range(count):
        before = randrange(1, 4)
        after = randrange(1, 3)
        frequency = ""
        
        for y in range(before):
            frequency += "%d"
        
        frequency += "."
        
        for z in range(after):
            frequency += "%d"
        
        frequencies.append(format_frequencies(frequency))
    
    return frequencies

def main():
    args = sys.argv[1:]
    
    if len(args) > 0:
        if "%d" in args[0]:
            if len(args) > 1:
                try:
                    count = int(args[1])
                    
                    for x in range(int(args[1])):
                        print format_frequencies(args[0])
                except ValueError:
                    print "%s isn't a number, ya dingus" % (args[1],)
            else:
                for x in range(3):
                    print format_frequencies(args[0])
        else:
            try:
                count = int(args[0])
                
                print "\n".join(generate_frequencies(count))
            except ValueError:
                print "%s yourself" % (args[0],)
    else:
        print "\n".join(generate_frequencies(3))

if __name__ == '__main__':
    main()
