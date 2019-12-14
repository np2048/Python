#!/usr/bin/python3

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Queue:
    def __init__(self):
        self.first = None
        self.last = None
        self.size = 0
    def push(self, data):
        node = Node(data)
        if self.first is None or self.last is None:
            self.first = node
            self.last = self.first
        else:
            self.last.next = node
            self.last = node
        self.size += 1
    def pop(self):
        if self.first is None:
            return None
        node = self.first
        self.first = node.next
        self.size -= 1
        return node
