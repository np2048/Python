#!/usr/bin/python3

#####################################################################
# try to add a test file data/addfile/newfile.txt
# to the directory data/addfile/target

import os
import sys
import shutil
from TestUtils import *

# Get file path of the current script
path = os.path.dirname( os.path.abspath( sys.argv[0] ))
subdir = os.path.splitext(os.path.basename( sys.argv[0] ) ) [0]
#print(subdir)
os.chdir(path)
#print(path)

# clean target directory
target = 'target'
pathDataShort   = os.sep+ 'data' +os.sep+ subdir +os.sep
pathData        = os.path.basename(path) + pathDataShort
pathDataAbs     = path + pathDataShort
filename        = 'newfile.txt'
pathNewFile     = pathData + filename
pathNewFileAbs  = pathDataAbs + filename
pathTarget      = pathData + target + os.sep
pathTargetAbs   = pathDataAbs + target + os.sep
#print(pathTargetAbs)
if os.path.isdir(pathTargetAbs) : shutil.rmtree(pathTargetAbs)

# run the script that is tested
pathScript = '..' + os.sep + os.path.basename( sys.argv[0])
#print(pathScript)
command = pathScript +' '+ pathTarget +' '+ pathNewFileAbs
#print(command)
os.system(command)

print('\nScript completed. Test results:')

# test if target path was created
print('Target directory: ', end='')
if not os.path.isdir(pathTargetAbs) : 
    PrintError('Fail')
    exit()
PrintSuccess("OK")

# test if new file was added
print('New file added to target directory: ', end='')
if not os.path.isfile(pathTargetAbs + filename) : 
    PrintError('Fail')
    exit()
PrintSuccess("OK")

# test if pathfile was added
print('New pathfile added: ', end='')
pathPathfile = pathTargetAbs + 'path' +os.sep+ filename
if not os.path.isfile(pathPathfile) : 
    PrintError('Fail')
    exit()
PrintSuccess("OK")

# test pathfile contents
print('New file path is correct: ', end='')
f = open(pathPathfile, 'r')
fileData = f.read()
f.close()
if not fileData == pathNewFileAbs : 
    PrintError('Fail')
    exit()
PrintSuccess("OK")

# now try to add the same file one more time
# to make sure that existing file will be saved
# with the name newfile.txt.old
os.system(command)
print('Backup existing file: ', end='')
if not os.path.isfile(pathTargetAbs + filename + '.old') : 
    PrintError('Fail')
    exit()
PrintSuccess("OK")

PrintSuccess("\nAll tests completed successfully!\n")