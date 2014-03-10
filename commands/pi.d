#!/usr/bin/env rdmd

import core.exception;
import std.stdio;
import std.conv;
import std.format;

void error(string message)
{
    writeln(message);
}

void main(string[] args)
{
    args = args[1..$];
    ulong precision, iterations;
    ulong counter = 1;
    double total = (4.0/counter);
    
    try
    {
        precision = to!ulong(args[0]);
    }
    catch(RangeError)
    {
        precision = 3;
    }
    catch(ConvOverflowException)
    {
        return error("Too much precision!");
    }
    catch(ConvException)
    {
        return error(to!string(args[0]) ~ " is not an integer/can't fit in a ulong.");
    }
    
    try
    {
        iterations = to!ulong(args[1]);
    }
    catch(RangeError)
    {
        iterations = 10000;
    }
    catch(ConvOverflowException)
    {
        return error("Too many iterations!");
    }
    catch(ConvException)
    {
        return error(to!string(args[1]) ~ " is not an integer/can't fit in a ulong.");
    }
    
    for(ulong iii = 0; iii < iterations; iii++)
    {
        counter += 2;
        total -= (4.0/counter);
        counter += 2;
        total += (4.0/counter);
    }
    
    writefln("%." ~ to!string(precision) ~ "f", total);
}
