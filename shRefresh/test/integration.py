#!/usr/bin/python3
import os
import sys
import shutil
from testUtils import * 

# try to install 1 test file

# Goto main script directory
os.chdir( os.path.dirname(os.path.dirname( os.path.abspath( sys.argv[0] ))) )

# remove target directory if exists
targetDir = Dir("target")
targetDir.remove()

# create test file
dataTestFiles = { "test1":"test1content", 'test2':'test2content' }
files = []
for fileName, fileContent in filesTest:
    testFile = File('.', fileName)
    testFile.write(fileContent)
    files.append(testFile)
    pathFile = File('path', fileName)
    pathFile.write(testFile.path() )

# run INSTALL
os.system("../refresh.py install")

# return error if target directory not created
if not targetDir.exists() 
   printError("No target directory")
   exit()

# return error if there are no test files in the target directory
filesTarget = []
for fileName, fileContent in dataTestFiles :
    fTarget = File(targetDir.path, testFile.name)
    if not fTarget.exists() :
        printError("File not installed")
        exit()
    filesTarget.append(fTarget)

# return error if target file content doesn't match
for testFile in filesTarget :
    testFileContent = testFile.read()
    if not testFileContent == dataTestFiles[testFile.name] :
       printError("File content doesn't match the target")
       exit()

printSuccess(sys.argv[0] + " OK")
