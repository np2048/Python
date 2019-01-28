#!/usr/bin/python3
import os
import sys
import shutil
from testUtils import * 

# test class File from testUtils

# test file data
newFileName = "test.file.txt"
newFileDir = 'test'
newFileContent = 'This is a test file'

# Additional data for test file
newFilePath = newFileDir + os.sep + newFileName
newFileDirAbsPath = os.path.abspath(newFileDir)
newFileAbsPath = newFileDirAbsPath + os.sep + newFileName

# delete test file and directory if exists
if os.path.exists(newFileDirAbsPath):
    shutil.rmtree(newFileDirAbsPath)

# Create new File class object
newFile = File(newFileDir, newFileName)

# test class methods
testName = 'path() : '
if not newFile.path() == newFilePath :
    printError("failed")
else :
    printSuccess("OK")

testName = 'abspath() : '
if not newFile.abspath() == newFileAbsPath :
    printError("failed")
else :
    printSuccess("OK")

