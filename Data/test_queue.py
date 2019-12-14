#!/usr/bin/python3

from queue import Queue

que = Queue()
i = 0
queSize = 1000000
for i in range(1, queSize+1) :
    que.push(i)

#print("i = {0}".format(i))

failCount = 0
for i in range(1, queSize+1) :
    n = que.pop()
    if n.data != i : failCount += 1

print("Queue {0} errors : {1}".format(queSize, failCount))
