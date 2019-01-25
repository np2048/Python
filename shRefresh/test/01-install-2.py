#!/usr/bin/python3
import os
import sys
import shutil
from testUtils import printError, printSuccess

# try to install 1 test file

# Goto main script directory
#os.chdir( os.path.dirname(os.path.dirname( os.path.abspath( sys.argv[0] ))) )

# remove target directory if exists
target = "target"
if os.path.exists("../" + target + "/"):
   shutil.rmtree("../" + target + "/")

# create test file
fileName = ["test1", "test2"]
fileContent = ["test1content", "test2content"]
for i in range(0, len(fileName)):
   os.system("./addFile.py " + fileName[i] + " " + fileContent[i] + " " + target)

# run INSTALL
#os.system("../refresh.py install")

# return error if target directory not created
if not os.path.exists("../" + target + "/"):
   printError("No target directory")
   exit()

# return error if no file1 int the target directory
def testFileExists(fileName, target):
   if not os.path.exists("../" + target + "/" + fileName):
      printError("File not installed")
      exit()
for i in range(0, len(fileName)):
   testFileExists(fileName[i], target)

# return error if targer file content doesn't match
def testFile(fileName, fileContent, target):
   targetFileContent=""
   with open("../" + target + "/" + fileName, "r") as f :
      targetFileContent = f.read()
   if not targetFileContent == fileContent :
      printError("File " + fileName + " content doesn't match the target")
      exit()
for i in range(0, len(fileName)):
   testFile(fileName[i], fileContent[i], target)

printSuccess(sys.argv[0] + " OK")
