#!/usr/bin/python3
import os
import sys
import shutil

# test Utilities module

def printError(message):
   print('\033[91m' + message + '\033[0m')

def printSuccess(message):
   print('\033[92m' + message + '\033[0m')

class File:
    def __init__(self, directory, name):
        self.directory = directory
        self.name = name
    def path(self):
        return self.directory + os.sep + self.name
    def abspath(self):
        return os.path.abspath(self.path)
    def exists(self):
        return os.path.exists(self.abspath() )
    def read(self):
        content = ''
        with open(self.path(), 'r') as hFile:
            content = hFile.readline()  
        return content
    def write(self, content):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        with open(self.path(), 'w') as hFile:
            hFile.write(content)

class Dir:
    def __init__(self, path):
        self.path = os.path.abspath(path)
        self.files = []
    def exists(self):
        return os.path.exists(self.path)
    def read(self):
        self.files = []
        if not self.exists():
            return
        for filename in os.listdir(self.path):
            self.files.append(File(self.path, filename) )
    def remove(self):
        if not self.exists():
            return
        shutil.rmtree(self.path)
        self.read()
    def addFile(self, fileName, fileContent):
        filePath = self.path + os.sep + fileName
        newFile = File(filePath)
        newFile.write(fileContent)
        self.files.append(newFile)
        return newFile


