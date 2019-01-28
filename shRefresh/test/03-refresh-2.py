#!/usr/bin/python3
import os
import sys
import shutil
from testUtils import printError, printSuccess

# try to install 1 test file
target = "target"

# Goto main script directory
#os.chdir( os.path.dirname(os.path.dirname( os.path.abspath( sys.argv[0] ))) )

# delete test file
fileName = ["test1", "test2"]
fileContent = ["test1content", "test2content"]
for name in fileName:
    os.remove("../" + name)

# run REFRESH
os.system("../refresh.py")

# return error if no file1 in current directory
def testFileExists(fileName):
   if not os.path.exists("../" + fileName):
      printError("File not refreshed")
      exit()
for name in fileName:
    testFileExists(name)

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
