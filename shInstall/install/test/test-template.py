#!/usr/bin/python3
import os
import sys
import shutil
import socket
from jinja2 import Template

from TestUtils import * 

# try to install test files

# remove target directory if exists
targetDir = Dir("target")
targetDir.Remove()

# create test file
dataDir = Dir("templates")
dataDir.Create()
dataTestFiles = { "config.txt":"Device: {{ device }}"}
hostname = socket.gethostname()
dataResultFiles = { "config.txt":"Device: " + hostname}
files = []
for fileName, fileContent in dataTestFiles.items():
    testFile = File(dataDir.path, fileName)
    testFile.Write(fileContent)
    files.append(testFile)
    pathFile = File(dataDir.path + os.sep + 'path', fileName)
    pathFile.Write(targetDir.path + os.sep + testFile.name)

# run INSTALL
os.system("../install.py test/" + dataDir.Name() )

# return error if target directory not created
if not targetDir.Exists():
    PrintError("1. No target directory")
    exit()

# return error if there are no test files in the target directory
filesTarget = []
for fileName, fileContent in dataTestFiles.items() :
    fTarget = File(targetDir.path, testFile.name)
    if not fTarget.Exists() :
        PrintError("2. File not installed")
        exit()
    filesTarget.append(fTarget)

# return error if target file content doesn't match
for testFile in filesTarget :
    testFileContent = testFile.Read()
    if not testFileContent == dataResultFiles[testFile.name] :
       PrintError("3. File content doesn't match the target")
       exit()

PrintSuccess(sys.argv[0] + " OK")
