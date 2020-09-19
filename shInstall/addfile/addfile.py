#!/usr/bin/python3

# This script is a part of config install framework
# It is used to add files into the config library
#
# Usage example: 
# ~ ./addfile.py program_name path_to_config_file/new_config_file_name
#
# If a file with the same name already exists in the library
# it will be renamed to <filename>.old
# If <filename>.old already exists it will be deleted.

import os
import sys
import shutil

def PrintSuccess(Action, FileName):
   print('\033[92m' + Action + '\033[0m ' + FileName)

def PrintGray(Action, FileName):
   print('\033[90m' + Action + ' ' + FileName + '\033[0m')

def PrintError(Action, FileName):
   print('\033[91m' + Action + '\033[0m ' + FileName)

# Create destination path
path = os.path.dirname( os.path.abspath( sys.argv[0] ))
pathDest = path + os.sep + sys.argv[1]
#print(pathDest)
os.makedirs(pathDest, exist_ok=True)

# If file with the same name already exists then
# save existent file as <filename>.old
filename = os.path.basename( sys.argv[2] )
pathDestFile = pathDest +os.sep+  filename
if os.path.isfile(pathDestFile) :
    pathDestFileOld = pathDestFile + '.old'
    if os.path.isfile(pathDestFileOld):
        os.remove(pathDestFileOld)
    os.rename(pathDestFile, pathDestFileOld)
    PrintGray('Backup', os.path.basename(pathDestFileOld))

# Copy new file to destination path
if not os.path.isfile(sys.argv[2]) : 
    PrintError("Incorrect file path", sys.argv[2])
    exit()
shutil.copyfile(sys.argv[2], pathDestFile)
PrintSuccess('Added', sys.argv[2])

# Create path directory
pathPath = pathDest + 'path' +os.sep
os.makedirs(pathPath, exist_ok=True)

# Create path file
filenamePath = pathPath + filename
f = open(filenamePath, 'w')
f.write(sys.argv[2])
f.close()