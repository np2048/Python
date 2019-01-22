#!/usr/bin/python3

import sys
from math import pi, sin
import numpy
import scipy.integrate as integrate

def f(radius):
   result = 0
   #result = integrate.quad(lambda x: 2 * radius * sin(1/2 * x), 0, 2*pi)

   return(result)

def f2(radius):
   step=10
   result = 0
   for i in range(0, step):
      a = 2 * pi * i / step
      result += 2*radius * sin( 1/2 * a)
      print("i:%i\na=%f\nresult=%f\n" % (i, a, result))
   return(result)

def print_usage():
    print("Usage:\n%s <radius>\nOutput: Length of a circle by a given radius\n\n" % sys.argv[0])



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
print("L(r=%f) = %f" % (num, res))
