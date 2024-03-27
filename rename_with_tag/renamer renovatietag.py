import os
import sys
import shutil

# this file has to be run from the folder where it has to archive the subfolders one by one

dlist = []
flist = []
for filename in os.listdir():
    if os.path.isdir(filename):
        dlist.append(filename)

print(os.getcwd())

l = len(dlist)
i = 0
for dir in dlist:
    y = dir[0:10] + " RENOVATIE" + dir[10:]
    print("-------------------")
    print("renaming from")
    print(dir)
    print("to")
    print(y)
    input("press enter to continue..")    
    os.rename(dir, y)
        
input("press enter to exit..")
