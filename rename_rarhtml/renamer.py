import os
import sys

def renamer():
	os.chdir("d:/temp")
	for filename in os.listdir():
		if "rar.html" in filename:
			print(filename +" -> " + filename[:-5])
			os.rename(filename, filename[:-5])

renamer()