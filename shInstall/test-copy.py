#!/usr/bin/python3
import os
import sys
import shutil
from TestUtils import * 

# try to install test files

# remove target directory if exists
TargetDir = Dir("target")
TargetDir.Remove()

# create test file
dataDir = Dir("data")
dataDir.Create()
dataTestFiles = { "test1":"test1content", 'test2':'test2content' }
files = []
for fileName, fileContent in dataTestFiles.items():
    testFile = File(dataDir.path, fileName)
    testFile.Write(fileContent)
    testFile.SetMode(0o777)
    files.append(testFile)
    pathFile = File(dataDir.path + os.sep + 'path', fileName)
    pathFile.Write(TargetDir.path + os.sep + testFile.name)

# run INSTALL
os.system("./install.py " + dataDir.Name() )

# return error if target directory not created
if not TargetDir.Exists():
    PrintError("1. No target directory")
    exit()

# return error if there are no test files in the target directory
filesTarget = []
for fileName, fileContent in dataTestFiles.items() :
    fTarget = File(TargetDir.path, testFile.name)
    if not fTarget.Exists() :
        PrintError("2. File not installed")
        exit()
    filesTarget.append(fTarget)

# return error if target file content doesn't match
for testFile in filesTarget :
    testFileContent = testFile.Read()
    if not testFileContent == dataTestFiles[testFile.name] :
       PrintError("3. File content doesn't match the target")
       exit()

# check file permissions (mode)
for testFile in filesTarget :
    testFileMode = testFile.GetMode()
    if not testFileMode == 0o777 :
       PrintError("4. File permissions doesn't match the target")
       exit()

# test backup function: run install once again, changed file has to be saved with ".default" postfix name
# modify target file contents
TargetFile = filesTarget[0]
BackupFileContent = "new content"
TargetFile.Write(BackupFileContent)
os.system("./install.py " + dataDir.Name() )

# .default file must exist
DefaultFile = File(TargetDir.path, TargetFile.name + '.default')
if not DefaultFile.Exists():
   PrintError("5. No .default backup file " + DefaultFile.Path() )
   exit()

# test default contents
if not DefaultFile.Read() == BackupFileContent :
    PrintError("6. default backup file content incorrect")
    exit()

PrintSuccess(sys.argv[0] + " OK")
