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
fileName = "test1"
fileContent = "test1content"
os.system("./addFile.py " + fileName + " " + fileContent + " " + target)

# run INSTALL
os.system("../refresh.py install")

# return error if target directory not created
if not os.path.exists("../" + target + "/"):
   printError("No target directory")
   exit()

# return error if no file1 int the target directory
if not os.path.exists("../" + target + "/" + fileName):
   printError("File not installed")
   exit()

# return error if targer file content doesn't match
targetFileContent=""
with open("../" + target + "/" + fileName, "r") as f :
   targetFileContent = f.read()
if not targetFileContent == fileContent :
   printError("File content doesn't match the target")
   exit()

printSuccess(sys.argv[0] + " OK")
