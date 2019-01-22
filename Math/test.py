#!/usr/bin/python3

import numpy

ans = numpy.float64(1.0)
for i in range(1, 30):
   ans = ans / 10 + i

print("ans: %f" % ans)
