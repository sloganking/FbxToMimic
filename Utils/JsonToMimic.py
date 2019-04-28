#Imports
#===========================================================================
import numpy as np
import math
import json
import os
from os import listdir
from os.path import isfile, join

# Function declarations
#===========================================================================

#Seems to be roll yaw pitch
def euler_to_quaternion(heading, attitude, bank):
    c1 = np.cos(heading/2)
    s1 = np.sin(heading/2)
    c2 = np.cos(attitude/2)
    s2 = np.sin(attitude/2)
    c3 = np.cos(bank/2)
    s3 = np.sin(bank/2)
    c1c2 = c1 * c2
    s1s2 = s1 * s2
    w = c1c2*c3 - s1s2*s3
    x = c1c2*s3 + s1s2*c3
    y = s1*c2*c3 + c1*s2*s3
    z = c1*s2*c3 - s1*c2*s3

    return [w,x,y,z]

def getTimesIn(obj):
    timeList = []

    # Loop though all animated items but not the time attribute
    for i in range(1,len(animated)):

        #Add all new times in item's T channel
        tSize = len(obj["Takes:"][f"Take:{onlyfiles[j][:-9]}"][animated[i]]["Channel:Transform"]["Channel:T"]["Channel:X"]["Key"])
        for x in range(0,tSize):
            tString = obj["Takes:"][f"Take:{onlyfiles[j][:-9]}"][animated[i]]["Channel:Transform"]["Channel:T"]["Channel:X"]["Key"][x]
            tTokens = tString.split(",")
            tTime = tTokens[0]
            if tTime not in timeList:
                timeList.append(tTime)

        #Add all new times in item's R channel
        rSize = len(obj["Takes:"][f"Take:{onlyfiles[j][:-9]}"][animated[i]]["Channel:Transform"]["Channel:R"]["Channel:X"]["Key"])
        for x in range(0,rSize):
            rString = obj["Takes:"][f"Take:{onlyfiles[j][:-9]}"][animated[i]]["Channel:Transform"]["Channel:R"]["Channel:X"]["Key"][x]
            rTokens = rString.split(",")
            rTime = rTokens[0]
            if rTime not in timeList:
                timeList.append(rTime)

    #Sorts list by integers
    timeList = sorted(timeList, key=int)

    return timeList

def timeInKey(time, key):
    #Create list of key Times
    keyTimes = []
    for x in range(0,len(key)):
        keyLineString = key[x]
        keyLineTokens = keyLineString.split(",")
        keyTimes.append(keyLineTokens[0])

    return time in keyTimes

def angleOfKeyAtTime(key, time):
    #Create list of key Times
    keyTimes = []
    for x in range(0,len(key)):
        keyLineString = key[x]
        keyLineTokens = keyLineString.split(",")
        keyTimes.append(keyLineTokens[0])

    if time in keyTimes:
        index = keyTimes.index(time)
        Tokens = key[index].split(",")
        angle = Tokens[1]
        return angle
    else:
        return False

def indexOfAnimated(anim):
    index = 0

    for i in range(0,len(animated)):
        if i < 2:   #skip non rotations
            index = index + 1
        elif fbxBoneName(deepMimicHumanoidJoints[i]) != anim:
            index = index + 1
        else:
            break
    
    return index

# Remove all files in given directory
def removeAllFilesInDirectory(directory):
    onlyfiles = [f for f in listdir(directory) if isfile(join(directory, f))]
    for i in range(0,len(onlyfiles)):
        os.remove(f"{directory}{onlyfiles[i]}")

def fbxBoneName(mimicBone):
    return humanoidRig[f"{mimicBone}"]

#Start of main program
#===========================================================================

#get json of humanoidRig
with open(f"./Rigs/humanoidRig.json") as json_data:
    humanoidRig = json.load(json_data)

print("Converting JSON to MimicMotion file")

# Initilize variables
animated = ["Seconds", "Model:Model::hip", "Model:Model::hip", "Model:Model::chest","Model:Model::neck","Model:Model::rThigh","Model:Model::rShin","Model:Model::rFoot","Model:Model::rShldr","Model:Model::rForeArm","Model:Model::lThigh","Model:Model::lShin","Model:Model::lFoot","Model:Model::lShldr","Model:Model::lForeArm"]
# Order is important
deepMimicHumanoidJoints = ["seconds", "hipPosition", "hip", "chest", "neck", "right hip", "right knee", "right ankle", "right shoulder", "right elbow", "left hip", "left knee", "left ankle", "left shoulder", "left elbow"]
dimensions = [1,3,4,4,4,4,1,4,4,1,4,1,4,4,1]
posLocked = True


string1 = "right knee"
print(f"Fbx right shen bone:       {fbxBoneName(string1)}")

mypath = "./Utils/Temp/"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]


print(f"Converting to MimicMotion:       {onlyfiles}")

for j in range(0,len(onlyfiles)):
    # Open files, Start of main program
    with open(f"./Utils/Temp/{onlyfiles[j]}") as json_data:
        with open(f"./OutputMimic/{onlyfiles[j]}.txt","w") as output:
            d = json.load(json_data)

            #File Header
            print(f"{{", file=output)
            print(f"\"Loop\": \"none\",", file=output)
            print(f"\"Frames\":", file=output)
            print(f"[", file=output)

            #Start of Keyframes
            listOfTimes = getTimesIn(d)
            
            #For every unique time, create a keyFrame
            keyFrame = []
            for i in range(0,len(listOfTimes)):
                print(f"Keyframe: {i}/{len(listOfTimes)}", end="\r")
                oldKeyframe = keyFrame
                keyFrame = []

                #Append Time
                if i == 0:      #If first time, use filler
                    keyFrame.append(int(listOfTimes[i]) * 0.00000000002)
                else:       # else calculate time based on previous times
                    keyFrame.append((int(listOfTimes[i]) - int(listOfTimes[i-1])) * 0.00000000002)

                #Append Root position
                if posLocked == False:
                    xKey = d["Takes:"][f"Take:{onlyfiles[j][:-9]}"][f"Model:Model::{fbxBoneName(deepMimicHumanoidJoints[2])}"]["Channel:Transform"]["Channel:T"]["Channel:X"]["Key"]
                    yKey = d["Takes:"][f"Take:{onlyfiles[j][:-9]}"][f"Model:Model::{fbxBoneName(deepMimicHumanoidJoints[2])}"]["Channel:Transform"]["Channel:T"]["Channel:Y"]["Key"]
                    zKey = d["Takes:"][f"Take:{onlyfiles[j][:-9]}"][f"Model:Model::{fbxBoneName(deepMimicHumanoidJoints[2])}"]["Channel:Transform"]["Channel:T"]["Channel:Z"]["Key"]

                    #If Keys contain angle for desired time
                    if angleOfKeyAtTime(xKey,listOfTimes[i]) and angleOfKeyAtTime(yKey,listOfTimes[i]) and angleOfKeyAtTime(zKey,listOfTimes[i]):

                        #Append angles
                        keyFrame.append(float(angleOfKeyAtTime(xKey,listOfTimes[i])))
                        keyFrame.append(float(angleOfKeyAtTime(yKey,listOfTimes[i])))
                        keyFrame.append(float(angleOfKeyAtTime(zKey,listOfTimes[i])))

                    # append old rotation
                    else:
                        keyFrame.append(oldKeyframe[1])
                        keyFrame.append(oldKeyframe[2])
                        keyFrame.append(oldKeyframe[3])

                #posLocked == true
                else:
                    keyFrame.append(0)
                    keyFrame.append(2)
                    keyFrame.append(0)

                #Append 1D and 4D rotations
                for x in range(0,len(deepMimicHumanoidJoints)):
                    if x > 1:   #skip seconds

                        #If posLocked, lock root rotation
                        if posLocked and x == 2:
                            keyFrame.append(1)
                            keyFrame.append(0)
                            keyFrame.append(0)
                            keyFrame.append(0)

                        else:
                            #if angle is 4D
                            if dimensions[x] == 4:
                                xKey = d["Takes:"][f"Take:{onlyfiles[j][:-9]}"][f"Model:Model::{fbxBoneName(deepMimicHumanoidJoints[x])}"]["Channel:Transform"]["Channel:R"]["Channel:X"]["Key"]
                                yKey = d["Takes:"][f"Take:{onlyfiles[j][:-9]}"][f"Model:Model::{fbxBoneName(deepMimicHumanoidJoints[x])}"]["Channel:Transform"]["Channel:R"]["Channel:Y"]["Key"]
                                zKey = d["Takes:"][f"Take:{onlyfiles[j][:-9]}"][f"Model:Model::{fbxBoneName(deepMimicHumanoidJoints[x])}"]["Channel:Transform"]["Channel:R"]["Channel:Z"]["Key"]

                                #If .fbx contains joint keyframe data for given time
                                if angleOfKeyAtTime(xKey,listOfTimes[i]) and angleOfKeyAtTime(yKey,listOfTimes[i]) and angleOfKeyAtTime(zKey,listOfTimes[i]):

                                    #Get angles
                                    X = float(angleOfKeyAtTime(xKey,listOfTimes[i]))
                                    Y = float(angleOfKeyAtTime(yKey,listOfTimes[i]))
                                    Z = float(angleOfKeyAtTime(zKey,listOfTimes[i]))

                                    # #Get angles
                                    # pitch = -X
                                    # yaw = -Y
                                    # roll = -Z

                                    if fbxBoneName(deepMimicHumanoidJoints[x]) == fbxBoneName('right shoulder'):
                                        pitch = Y - 20
                                        yaw = X
                                        roll = Z - 83
                                    elif fbxBoneName(deepMimicHumanoidJoints[x]) == fbxBoneName('left shoulder'):
                                        pitch = Y
                                        yaw = X 
                                        roll = Z + 83
                                    elif fbxBoneName(deepMimicHumanoidJoints[x]) == fbxBoneName('right hip') or fbxBoneName(deepMimicHumanoidJoints[x]) == fbxBoneName('left hip'):
                                        pitch = Y - 55
                                        yaw = X
                                        roll = Z
                                    elif fbxBoneName(deepMimicHumanoidJoints[x]) == fbxBoneName('right ankle'):
                                        pitch = Y - 70
                                        yaw = X + 35
                                        roll = Z + 45
                                    elif fbxBoneName(deepMimicHumanoidJoints[x]) == fbxBoneName('left ankle'):
                                        pitch = Y - 70
                                        yaw = X - 35
                                        roll = Z - 45
                                    else:
                                        pitch = Y
                                        yaw = X
                                        roll = Z

                                    #Zero out things for testing
                                    #pitch = 0
                                    #yaw = 0
                                    #roll = 0

                                    #Invert needed things
                                    pitch = -pitch
                                    yaw = -yaw
                                    roll = roll 

                                    #Calculate quaternion angle
                                    quat = euler_to_quaternion(math.radians(yaw), math.radians(pitch), math.radians(roll))

                                    #Append quaternion angle
                                    keyFrame.append(quat[0])
                                    keyFrame.append(quat[1])
                                    keyFrame.append(quat[2])
                                    keyFrame.append(quat[3])

                                else:
                                    animIndex = indexOfAnimated(fbxBoneName(deepMimicHumanoidJoints[x]))

                                    for i in range(0,4):
                                        keyFrame.append(oldKeyframe[animIndex + i])

                            #If angle is 1D (Knees and elbows)
                            elif dimensions[x] == 1:
                                    #If Knees
                                    if fbxBoneName(deepMimicHumanoidJoints[x]) == fbxBoneName('right knee') or fbxBoneName(deepMimicHumanoidJoints[x]) == fbxBoneName('left knee'):

                                        #if angle found, append
                                        #Should be channel X (Unity knee bend) but takes channel Y for some reason
                                        #Perhaps unity reads Y as it's X
                                        xKey = d["Takes:"][f"Take:{onlyfiles[j][:-9]}"][f"Model:Model::{fbxBoneName(deepMimicHumanoidJoints[x])}"]["Channel:Transform"]["Channel:R"]["Channel:Y"]["Key"]
                                        if angleOfKeyAtTime(xKey,listOfTimes[i]):
                                            X = math.radians(float(angleOfKeyAtTime(xKey,listOfTimes[i])))
                                            keyFrame.append(X)

                                        #else append last angle
                                        else:
                                            keyFrame.append(oldKeyframe[x])

                                    #If Elbow
                                    elif fbxBoneName(deepMimicHumanoidJoints[x]) == fbxBoneName('right elbow') or fbxBoneName(deepMimicHumanoidJoints[x]) == fbxBoneName('left elbow'):

                                        #if angle found, append
                                        yKey = d["Takes:"][f"Take:{onlyfiles[j][:-9]}"][f"Model:Model::{fbxBoneName(deepMimicHumanoidJoints[x])}"]["Channel:Transform"]["Channel:R"]["Channel:Y"]["Key"]
                                        if angleOfKeyAtTime(yKey,listOfTimes[i]):
                                            Y = -math.radians(float(angleOfKeyAtTime(yKey,listOfTimes[i])))
                                            
                                            keyFrame.append(Y)

                                        #else append last angle
                                        else:
                                            keyFrame.append(oldKeyframe[x])
                                        
                                    else:
                                        print(f"Error 1D rotation but type not specified")
                            else:
                                print(f"Error on rotations Loop {x}")

                #Turn keyFrame into a recordable JSON String
                keyFrameString = "["
                keyFrameString += str(keyFrame[0])

                for x in range(0,len(keyFrame)):
                    if x > 0:
                        keyFrameString += ","
                        keyFrameString += str(keyFrame[x])

                #Put comma at end of all keyFrame lines but the last
                keyFrameString += "]"
                if i < len(listOfTimes) - 1:
                    keyFrameString += ","

                print(f"{keyFrameString}", file=output)

            #Close JSON object
            print(f"]", file=output)
            print(f"}}", file=output)

            print(f"MimicMotion {onlyfiles[j]}.txt created")

#removeAllFilesInDirectory("./Utils/Temp/")