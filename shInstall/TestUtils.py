#!/usr/bin/python3
import os
import sys
import shutil
import stat

# test Utilities module

def PrintError(message):
   print('\033[91m' + message + '\033[0m')

def PrintSuccess(message):
   print('\033[92m' + message + '\033[0m')

class File:
    def __init__(self, directory, name):
        self.dir = directory
        self.name = name
    def Path(self):
        return self.dir + os.sep + self.name
    def Abspath(self):
        return os.path.abspath(self.dir)
    def Exists(self):
        return os.path.exists(self.Path() )
    def Read(self):
        content = ''
        if not self.Exists() : 
            return content
        with open(self.Path(), 'r') as hFile:
            content = hFile.readline()  
        return content
    def Write(self, new_content):
        old_content = self.Read()
        if old_content == new_content and self.Exists(): 
            return
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)
        with open(self.Path(), 'w') as hFile:
            hFile.write(new_content)
    def SetMode(self, new_mode):
        os.chmod(self.Path(), new_mode)
        return
    def GetMode(self):
        mode = os.stat(self.Path())[stat.ST_MODE] - 0o100000
        return mode

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


