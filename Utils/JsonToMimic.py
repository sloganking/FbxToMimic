import numpy as np
import math
import json
import os
from os import listdir
from os.path import isfile, join

# Function declarations
def euler_to_quaternion(roll, pitch, yaw):
    qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
    qx = np.sin(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) - np.cos(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
    qy = np.cos(roll/2) * np.sin(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.cos(pitch/2) * np.sin(yaw/2)
    qz = np.cos(roll/2) * np.cos(pitch/2) * np.sin(yaw/2) - np.sin(roll/2) * np.sin(pitch/2) * np.cos(yaw/2)
    return [qw, qx, qy, qz]

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
        if animated[i] != anim:
            index = index + 1
        else:
            break
    
    return index

print("Converting JSON to MimicMotion file")

# Initilize variables
animated = ["Seconds", "Model:Model::hip", "Model:Model::hip", "Model:Model::chest","Model:Model::neck","Model:Model::rThigh","Model:Model::rShin","Model:Model::rFoot","Model:Model::rShldr","Model:Model::rForeArm","Model:Model::lThigh","Model:Model::lShin","Model:Model::lFoot","Model:Model::lShldr","Model:Model::lForeArm"]
dimensions = [1,3,4,4,4,4,1,4,4,1,4,1,4,4,1]
posLocked = True

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
                oldKeyframe = keyFrame
                keyFrame = []

                #Append Time
                if i == 0:
                    keyFrame.append(int(listOfTimes[i]) * 0.00000000002)
                else:
                    keyFrame.append((int(listOfTimes[i]) - int(listOfTimes[i-1])) * 0.00000000002)


                if posLocked == False:
                    # #Append Root position
                    xKey = d["Takes:"][f"Take:{onlyfiles[j][:-9]}"]["Model:Model::hip"]["Channel:Transform"]["Channel:T"]["Channel:X"]["Key"]
                    yKey = d["Takes:"][f"Take:{onlyfiles[j][:-9]}"]["Model:Model::hip"]["Channel:Transform"]["Channel:T"]["Channel:Y"]["Key"]
                    zKey = d["Takes:"][f"Take:{onlyfiles[j][:-9]}"]["Model:Model::hip"]["Channel:Transform"]["Channel:T"]["Channel:Z"]["Key"]

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
                for x in range(0,len(animated)):
                    if x > 1:

                        #If posLocked, lock root rotation
                        if posLocked and x == 2:
                            keyFrame.append(1)
                            keyFrame.append(0)
                            keyFrame.append(0)
                            keyFrame.append(0)

                        else:
                            #if angle is 4D
                            if dimensions[x] == 4:
                                xKey = d["Takes:"][f"Take:{onlyfiles[j][:-9]}"][animated[x]]["Channel:Transform"]["Channel:R"]["Channel:X"]["Key"]
                                yKey = d["Takes:"][f"Take:{onlyfiles[j][:-9]}"][animated[x]]["Channel:Transform"]["Channel:R"]["Channel:Y"]["Key"]
                                zKey = d["Takes:"][f"Take:{onlyfiles[j][:-9]}"][animated[x]]["Channel:Transform"]["Channel:R"]["Channel:Z"]["Key"]

                                if angleOfKeyAtTime(xKey,listOfTimes[i]) and angleOfKeyAtTime(yKey,listOfTimes[i]) and angleOfKeyAtTime(zKey,listOfTimes[i]):

                                    #Get angles
                                    X = float(angleOfKeyAtTime(xKey,listOfTimes[i]))
                                    Y = float(angleOfKeyAtTime(yKey,listOfTimes[i]))
                                    Z = float(angleOfKeyAtTime(zKey,listOfTimes[i]))

                                    #Calculate quaternion angle
                                    quat = euler_to_quaternion(math.radians(-Z), math.radians(-Y), math.radians(-X))

                                    #Append quaternion angle
                                    keyFrame.append(quat[0])
                                    keyFrame.append(quat[1])
                                    keyFrame.append(quat[2])
                                    keyFrame.append(quat[3])

                                else:
                                    animIndex = indexOfAnimated(animated[x])

                                    for i in range(0,4):
                                        keyFrame.append(oldKeyframe[animIndex + i])

                            #If angle is 1D (Knees and elbows)
                            elif dimensions[x] == 1:

                                    #If Knees
                                    if animated[x] == "Model:Model::rShin" or animated[x] == "Model:Model::lShin":

                                        #if angle found, append
                                        xKey = d["Takes:"][f"Take:{onlyfiles[j][:-9]}"][animated[x]]["Channel:Transform"]["Channel:R"]["Channel:X"]["Key"]
                                        if angleOfKeyAtTime(xKey,listOfTimes[i]):
                                            X = math.radians(float(angleOfKeyAtTime(xKey,listOfTimes[i])))
                                            keyFrame.append(X)

                                        #else append last angle
                                        else:
                                            keyFrame.append(oldKeyframe[x])

                                    #If Elbows
                                    elif animated[x] == "Model:Model::rForeArm" or animated[x] == "Model:Model::lForeArm":

                                        #if angle found, append
                                        yKey = d["Takes:"][f"Take:{onlyfiles[j][:-9]}"][animated[x]]["Channel:Transform"]["Channel:R"]["Channel:Y"]["Key"]
                                        if angleOfKeyAtTime(yKey,listOfTimes[i]):
                                            Y = math.radians(float(angleOfKeyAtTime(xKey,listOfTimes[i])))
                                            keyFrame.append(Y)

                                        #else append last angle
                                        else:
                                            keyFrame.append(oldKeyframe[x])
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

            # # Remove all files in "./Utils/Temp/"
            # mypath = "./Utils/Temp/"
            # onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
            # for i in range(0,len(onlyfiles)):
            #     os.remove(f"{mypath}{onlyfiles[i]}")