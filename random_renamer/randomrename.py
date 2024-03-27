'''
Created on 1-jan.-2014

@author: jorrit
'''


import os
import random

filelist = os.listdir()
for file in filelist:
    if file == "randomrename.py":
        continue

    rand = random.randint(1000000,2000000)
    newname = str(rand)+".jpg"

    print("renaming "+file+" to "+newname)
    os.rename(file,newname)
    
input("enter to quit...")
    