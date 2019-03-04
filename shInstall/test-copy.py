#!/usr/bin/python3
import os
import sys
import shutil
import subprocess
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
BackupFile = File(TargetDir.path, TargetFile.name + '.default')
if not BackupFile.Exists():
   PrintError("5. No .default backup file " + BackupFile.Path() )
   exit()

# test default contents
if not BackupFile.Read() == BackupFileContent :
    PrintError("6. default backup file content incorrect")
    exit()

# do the same test but this time use .old backup file name
# modify target file contents
BackupFileContent = "new content"
TargetFile.Write(BackupFileContent)
os.system("./install.py " + dataDir.Name() )

# .default file must exist
BackupFile = File(TargetDir.path, TargetFile.name + '.old')
if not BackupFile.Exists():
   PrintError("7. No .old backup file " + BackupFile.Path() )
   exit()

# test default contents
if not BackupFile.Read() == BackupFileContent :
    PrintError("8. old backup file content incorrect")
    exit()

# run install script one again and make sure there is now WRITE message as log output
# (target file already exists and is the same, so no rewrite is needed
result = subprocess.run(["./install.py", dataDir.Name()], stdout=subprocess.PIPE)
result = result.stdout.decode('utf-8')
if result != '':
    PrintError("9. Extra output (no changes were made after last run):")
    print(result)
    exit()

PrintSuccess(sys.argv[0] + " OK")
