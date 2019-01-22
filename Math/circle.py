#!/usr/bin/python3

import sys
from math import pi
import numpy
import scipy.integrate as integrate

def f(radius):
   #result = integrate.quad(lambda x: 2*pi * x, 0, radius)
   result = integrate.quad(lambda x: 0.5 * radius, 0, 2*pi*radius)
   return(result[0])

def print_usage():
    print("Usage:\n%s <radius>\nOutput: Area of a circle by a given radius\n\n" % sys.argv[0])



############################################################
# Get arguments

try:
    num = float(sys.argv[1])
except:
    print_usage()
    exit()


############################################################
# Main program starts here

res = f(num)
print("S(r=%f) = %f" % (num, res))
