#!/usr/bin/python3
import os
import sys
import shutil

# test Utilities module

def PrintError(message):
   print('\033[91m' + message + '\033[0m')

def PrintSuccess(message):
   print('\033[92m' + message + '\033[0m')

class File:
    def __init__(self, directory, name):
        self.directory = directory
        self.name = name
    def Path(self):
        return self.directory + os.sep + self.name
    def Abspath(self):
        return os.path.abspath(self.path)
    def Exists(self):
        return os.path.exists(self.abspath() )
    def Read(self):
        content = ''
        with open(self.path(), 'r') as hFile:
            content = hFile.readline()  
        return content
    def Write(self, content):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        with open(self.path(), 'w') as hFile:
            hFile.write(content)

class Dir:
    def __init__(self, path):
        self.path = os.path.abspath(path)
        self.files = []
    def Exists(self):
        return os.path.exists(self.path)
    def Create(self):
        if not self.Exists(): 
            os.makedirs(self.path)
    def Name(self):
        return os.path.basename(self.path)
    def Read(self):
        self.files = []
        if not self.Exists():
            return
        for filename in os.listdir(self.path):
            self.files.append(File(self.path, filename) )
    def Remove(self):
        if not self.Exists():
            return
        shutil.rmtree(self.path)
        self.Read()
    def AddFile(self, fileName, fileContent):
        filePath = self.path + os.sep + fileName
        newFile = File(filePath)
        newFile.write(fileContent)
        self.files.append(newFile)
        return newFile


