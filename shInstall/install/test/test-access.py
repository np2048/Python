#!/usr/bin/python3
import os
import sys
import shutil
import datetime

from TestUtils import * 

# try to install test files
targetDir = Dir('/tmp')
targetFile = File(targetDir.path, 'root.txt')
if not targetFile.Exists() : targetFile.Write('test')
targetFile.SetMode(0o444)
timeFile = File(targetDir.path, 'time.txt')

# create test file
dataDir = Dir("data")
dataDir.Create()
Now = str(datetime.datetime.now())
dataTestFiles = { "root.txt":"Root: {{ root }}", "time.txt":Now}
dataResultFiles = { "root.txt" : "Root: ", "time.txt":Now }
files = []
for fileName, fileContent in dataTestFiles.items():
    testFile = File(dataDir.path, fileName)
    if testFile.Exists() : testFile.SetMode(0o777)
    testFile.Write(fileContent)
    testFile.SetMode(0o444)
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
