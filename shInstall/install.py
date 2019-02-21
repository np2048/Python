#!/usr/bin/python3

# This script is for copying the files to the current directory from the system.
# The actual path of the original files should be stored in the "path/" subdirectory.
# The name of a file in the "path/" subdirectory matches the copyed file name.

# If run with "install" argument it will copy the files from local directory TO the system.

import os
import sys
import socket
from jinja2 import Template


class Dir:
    def __init__(self, path):
        self.path = path
        self.read()
    def Install(self):
        for filename, filepath in self.files.items():
            dirpath = os.path.dirname(filepath )
            self.CopyFile(filename, filepath)
    def CopyFile(self, SourcePath, TargetPath):
        SourceContent = self.RenderFile(SourcePath)
        print("Write: " + TargetPath)
        self.WriteFile(TargetPath, SourceContent)
    def RenderFile(self, Path):
        Content = self.ReadFile(Path) # read source file
        template = Template(Content) # render source file using template engine
        hostname = socket.gethostname() # Get PC name
        Content = template.render(device=hostname)
        return Content
    def WriteFile(self, Path, NewContent):
        OldContent = self.ReadFile(Path)
        if OldContent == NewContent and os.path.exists(Path) :
            return
        PathDir = os.path.dirname(Path) 
        if not os.path.exists( PathDir ):
            os.makedirs( PathDir )
        with open(Path, 'w') as hFile:
            hFile.write(NewContent)
    def ReadFile(self, Path):
        content = ''
        if not os.path.exists(Path) : 
            return content
        with open(Path, 'r') as hFile:
            content = hFile.read()  
        return content
# Go throu all the files in the path/ subdirectory. 
# Every file in path/ contains the actual path of the orignal file in the system.
    def read(self):
        PathDirName = 'path'
        self.files = { }
        os.chdir(self.path)
        if not os.path.exists(PathDirName) :
           return
        for filename in os.listdir(PathDirName):
            with open(PathDirName+ os.sep +filename, 'r') as fPath:
                self.files.update({filename : os.path.expanduser( fPath.readline().replace('\n', '').replace('\r', '') ) } )
#print(self.files)
    def system(self, command):
        print(command, end=' ')
        try:
            os.system(command)
        except :
            print("error: " + command)
        print("")
   
#main run
DirName = os.path.dirname( os.path.abspath( sys.argv[0] )) 
if (len(sys.argv) > 1 and sys.argv[1] != '') :
    DirName += os.sep + sys.argv[1]
currentDir = Dir(DirName)
currentDir.Install()

