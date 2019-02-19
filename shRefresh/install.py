#!/usr/bin/python3

# This script is for copying the files to the current directory from the system.
# The actual path of the original files should be stored in the "path/" subdirectory.
# The name of a file in the "path/" subdirectory matches the copyed file name.

# If run with "install" argument it will copy the files from local directory TO the system.

import os
import sys

class Dir:
   def __init__(self, path):
      self.path = path
      self.read()

   def Install(self):
      for filename, filepath in self.files.items():
         self.system('mkdir -p ' + os.path.dirname(filepath))
         self.system("cp " + filename + " " + filepath ) 
   
   # Go throu all the files in the path/ subdirectory. 
   # Every file in path/ contains the actual path of the orignal file in the system.
   def read(self):
      self.files = { }
      os.chdir(self.path)
      for filename in os.listdir('path'):
         with open('path'+ os.sep +filename, 'r') as fPath:
            self.files.update({filename : fPath.readline().replace('\n', '').replace('\r', '')} )
      #print(self.files)

   def system(self, command):
      print(command, end=' ')
      try:
         os.system(command)
      except :
          print("error: " + command)
      print("")
   
#main run
DirName = os.path.dirname(sys.argv[0]) 
if (sys.argv[1] != '') :
    currentDir += os.sep + sys.argv[1]
currentDir = Dir(DirName)
currentDir.Install()

