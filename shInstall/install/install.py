#!/usr/bin/python3

# This script if for copying config files stored in the library to the system.
# "Library" is actually the current directory. 
# Config files for a program are stored in subdirectories. 
#
# For example: if you have your vim configs in the vim subdirectory you may
# run "./install.py vim" and all the files from vim subdirectory will be
# copied to their destination paths. The destination paths of all files 
# to copy in this example should be stored in the vim/path subdirectory.
# 
# To add a file to this library run ./addfile.py <dir> <file_path>
# For example to add vim config to the library run:
# ./addfile vim ~/.vimrc



#####################################################################
# Global variables

# Files with the following extensions won't be processed by the
# template engine. Insted of this they will be just copyed "as is"
TemplateIgnoreExt = ['.lua', '.png', '.jpg', '.jpeg', 'otf']

# Try to create symbolic links instead of copying files if True.
# Value will be set to True if -l or --list argument is passed.
argvLink = False



#####################################################################
# Core code

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
        if not self.WriteFile(TargetPath, SourceContent): return
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
        # render file using Jinja if it is not a Lua file.
        # Lua's syntax is not compatible with Jinja as it contains multiple {{ strings
        if os.path.splitext(Path)[1] in TemplateIgnoreExt :
            return Content
        template = Template(Content, trim_blocks=True) # render source file using template engine
        hostname = socket.gethostname() # Get PC name
        Content = template.render(device=hostname)
        return Content
    def WriteFile(self, Path, NewContent):
        OldContent = self.ReadFile(Path)
        if OldContent == NewContent and os.path.isfile(Path) :
            return False
        PathDir = os.path.dirname(Path) 
        if not os.path.exists( PathDir ):
            os.makedirs( PathDir )
        if OldContent != '' and os.path.isfile(Path) :
            self.BackupFile(Path)
        result = False
        try:
            with open(Path, 'w') as hFile:
                hFile.write(NewContent)
            PrintSuccess("Write", Path)
            result = True
        except: PrintError("No write access", Path)
        return result
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
            print("Error: " + command)
        print("")
   


#####################################################################
# main run
#####################################################################

# Process arguments
argvSet = set(sys.argv[1:])
if '--help' in argvSet or '-h' in argvSet :
    print(  
        "\nUsage: %(app)s SUBDIRECTORY [OPTIONS]\n"
        "\tSUBDIRECTORY\tname of a subdirectory at %(app_name)s path\n"
        "\t-l, --link\tTry to create symlinks instead of copying when possible\n"
        "\n"
        "Symbolic link can be added only when no Jinja tags are used in a file\n"
        "and file owner of the source matches to the destination file.\n"
        % { 'app' : sys.argv[0], 
            'app_name' : os.path.basename(sys.argv[0]) }
    )
    exit(1)

if '--link' in argvSet :
    argvLink = True
    argvSet.remove('--link')
if '-l' in argvSet :
    argvLink = True
    argvSet.remove('-l')
#if argvLink : print("Link")

argvPath = ''
argvList = list(argvSet)
if len(argvList) > 0 :
    argvPath = argvList[0]
if not argvPath :
    print(  
        "%(app)s: missing operand\n"
        "Try '%(app)s --help' for more information."
        % {'app' : sys.argv[0] }
    )
    exit(1)

# Get path of current script
DirName = os.path.dirname( os.path.abspath( sys.argv[0] )) 

# Add argument to current path
if (argvPath) :
    DirName += os.sep + argvPath

# run dir.install procedure
currentDir = Dir(DirName)
currentDir.Install()

