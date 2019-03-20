import numpy as np
import math
import json

def euler_to_quaternion(roll, pitch, yaw):

    qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
    qx = np.sin(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) - np.cos(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
    qy = np.cos(roll/2) * np.sin(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.cos(pitch/2) * np.sin(yaw/2)
    qz = np.cos(roll/2) * np.cos(pitch/2) * np.sin(yaw/2) - np.sin(roll/2) * np.sin(pitch/2) * np.cos(yaw/2)

    return [qw, qx, qy, qz]

# yaw, pitch, roll

#Seems to be roll yaw pitch
def euler_to_quaternion2(heading, attitude, bank):
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


# initialize variables
animated = ["Seconds", "Model:Model::hip", "Model:Model::hip", "Model:Model::chest","Model:Model::neck","Model:Model::rThigh","Model:Model::rShin","Model:Model::rFoot","Model:Model::rShldr","Model:Model::rForeArm","Model:Model::lThigh","Model:Model::lShin","Model:Model::lFoot","Model:Model::lShldr","Model:Model::lForeArm"]
dimensions = [1,3,4,4,4,4,1,4,4,1,4,1,4,4,1]

testedJoint = "Model:Model::rShldr"
testedJoint = "Model:Model::rThigh"


with open("19_15.fbx.json.txt","w") as output:

    #File Header
    print(f"{{", file=output)
    print(f"\"Loop\": \"none\",", file=output)
    print(f"\"Frames\":", file=output)
    print(f"[", file=output)

    keyFrame = []
    for i in range(0,len(animated)):

        #==========================================================

        #if custom joint, animate
        if animated[i] == testedJoint:
            #keyFrame.append(-math.radians(45))

            #Unity's angles
            X = 0
            Y = 0
            Z = 90 + 45

            #Unity's angles (rThigh)
            X = -69
            Y = -28
            Z = 30

            # TestQuat = quat = euler_to_quaternion2(math.radians(X), math.radians(Y), math.radians(Z))
            # print(f"Test Quat:     {TestQuat}")

            pitch = -X
            yaw = -Y
            roll = -Z

            # #Get unity angles
            # X = UZ
            # Y = UY
            # Z = UX

            #yaw,pitch,roll
            quat = euler_to_quaternion2(math.radians(yaw), math.radians(pitch), math.radians(roll))
            #quat[3] = quat[3] * -1
            print(f"Regular Quat:     {quat}")

            # #Calculate quaternion angle
            # quat = euler_to_quaternion(math.radians(-Z), math.radians(-Y), math.radians(-X))
            #print(f"Weird Quat:     {quat}")

            #Append quaternion angle
            keyFrame.append(quat[0])
            keyFrame.append(quat[1])
            keyFrame.append(quat[2])
            keyFrame.append(quat[3])

        #==========================================================
        #if time
        elif i == 0:
            keyFrame.append(0.0333320000)
        #if root position
        elif i == 1:
            #XYZ
            keyFrame.append(0)
            keyFrame.append(2)
            keyFrame.append(0)
        elif dimensions[i] == 4:
            keyFrame.append(1)
            keyFrame.append(0)
            keyFrame.append(0)
            keyFrame.append(0)
        elif dimensions[i] == 1:
            keyFrame.append(0)

    #Turn keyFrame into a recordable JSON String
    keyFrameString = "["
    keyFrameString += str(keyFrame[0])

    for x in range(0,len(keyFrame)):
        if x > 0:
            keyFrameString += ","
            keyFrameString += str(keyFrame[x])
    keyFrameString += "]"

    print(f"{keyFrameString},", file=output)
    print(f"{keyFrameString},", file=output)
    print(f"{keyFrameString}", file=output)

    #Close JSON object
    print(f"]", file=output)
    print(f"}}", file=output)

    print(f"MimicMotion.txt created")