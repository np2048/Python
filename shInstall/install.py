#!/usr/bin/python3

# This script is for copying the files to the current directory from the system.
# The actual path of the original files should be stored in the "path/" subdirectory.
# The name of a file in the "path/" subdirectory matches the copyed file name.

# If run with "install" argument it will copy the files from local directory TO the system.

import os
import stat
import sys
import shutil
import socket
from jinja2 import Template

def PrintSuccess(Action, FileName):
   print('\033[92m' + Action + '\033[0m ' + FileName)

def PrintGray(Action, FileName):
   print('\033[90m' + Action + ' ' + FileName + '\033[0m')

def PrintError(Action, FileName):
   print('\033[91m' + Action + '\033[0m ' + FileName)

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
        if SourceContent == '' : return
        self.WriteFile(TargetPath, SourceContent)
        self.CopyFileMode(SourcePath, TargetPath)
    def CopyFileMode(self, SourcePath, TargetPath):
        SourceMode = self.GetFileMode(SourcePath)
        if SourceMode != self.GetFileMode(TargetPath) :
            try: os.chmod(TargetPath, SourceMode)
            except: PrintError("No chmod access", TargetPath)
    def GetFileMode(self, SourcePath):
        result = False
        try: result = os.stat(SourcePath)[stat.ST_MODE]
        except: PrintError("No read access", SourcePath)
        return result
    def RenderFile(self, Path):
        Content = self.ReadFile(Path) # read source file
        template = Template(Content, trim_blocks=True) # render source file using template engine
        hostname = socket.gethostname() # Get PC name
        Content = template.render(device=hostname)
        return Content
    def WriteFile(self, Path, NewContent):
        OldContent = self.ReadFile(Path)
        if OldContent == NewContent and os.path.isfile(Path) :
            return
        PathDir = os.path.dirname(Path) 
        if not os.path.exists( PathDir ):
            os.makedirs( PathDir )
        if OldContent != '' and os.path.isfile(Path) :
            self.BackupFile(Path)
        try:
            with open(Path, 'w') as hFile:
                hFile.write(NewContent)
            PrintSuccess("Write", Path)
        except: PrintError("No write access", Path)
    def BackupFile(self, Path):
        if os.path.exists(Path) :   # if a file already exists save it before overwrite 
            BackupFileName = Path + '.old'
            DefaultBackupFileName = Path + '.default'
            if not os.path.exists(DefaultBackupFileName):
                # if no default backup but .old exists rename old file to be the .default
                if os.path.exists(BackupFileName): 
#                    try :
                        shutil.move(BackupFileName, DefaultBackupFileName)
                        PrintGray("Make default", os.path.basename(BackupFileName) 
                                + ' > ' + os.path.basename(DefaultBackupFileName))
#                    except:
#                        PrintError("No access", BackupFileName + ' > ' + DefaultBackupFileName)
                else :
                    BackupFileName = DefaultBackupFileName
            try:
                shutil.move(Path, BackupFileName)
                PrintGray("Backup", BackupFileName)
            except: PrintError("No access", Path + ' > ' + BackupFileName)
    def ReadFile(self, Path):
        content = ''
        if not os.path.exists(Path) : 
            return content
        try:
            with open(Path, 'r') as hFile:
                content = hFile.read()  
        except: PrintError("No read access", Path)
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

