#!/usr/bin/python3

import sys

def f(num):
    result = 0
    if num > 1 : 
        result = num * f(num-1)
    else : 
        result = 1
    return result

def print_usage():
    print("Usage:\n%s <integer>\n\nInteger argument should be greater than 0\n" % sys.argv[0])



############################################################
# Get arguments

try:
    num = int(sys.argv[1])
except:
    print_usage()
    exit()

if num <= 0:
    print_usage()
    exit()

############################################################
# Main program starts here

fact = f(num)
print("%i! = %i" % (num, fact))
 
