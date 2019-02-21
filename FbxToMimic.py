import os
from os import listdir
from os.path import isfile, join

# Remove all files in "./OutputMimic"
mypath = "./OutputMimic/"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
for i in range(0,len(onlyfiles)):
    os.remove(f"{mypath}{onlyfiles[i]}")

os.system("python ./Utils/FbxToJson.py")
os.system("python ./Utils/JsonToMimic.py")