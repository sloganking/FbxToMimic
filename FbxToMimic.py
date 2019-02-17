import numpy as np
import math

def euler_to_quaternion(roll, pitch, yaw):

    qx = np.sin(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) - np.cos(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
    qy = np.cos(roll/2) * np.sin(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.cos(pitch/2) * np.sin(yaw/2)
    qz = np.cos(roll/2) * np.cos(pitch/2) * np.sin(yaw/2) - np.sin(roll/2) * np.sin(pitch/2) * np.cos(yaw/2)
    qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)

    return [qx, qy, qz, qw]

def quaternion_to_euler(x, y, z, w):

    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + y * y)
    #X = math.degrees(math.atan2(t0, t1))
    X = math.atan2(t0, t1)

    t2 = +2.0 * (w * y - z * x)
    t2 = +1.0 if t2 > +1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    #Y = math.degrees(math.asin(t2))
    Y = math.asin(t2)

    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y * y + z * z)
    #Z = math.degrees(math.atan2(t3, t4))
    Z = math.atan2(t3, t4)

    return X, Y, Z

euler_Original = (np.random.random(3) * 1).tolist() # Generate random rotation angles for XYZ within the range [0, 360)
quat = euler_to_quaternion(euler_Original[0], euler_Original[1], euler_Original[2]) # Convert to Quaternion
newEulerRot = quaternion_to_euler(quat[0], quat[1], quat[2], quat[3]) #Convert the Quaternion to Euler angles

# print ("Euler: ")
# print (euler_Original)
# print ("quat: ")
# print (quat)
# print ("Final Euler: ")
# print (newEulerRot)

import json
with open('./rThigh.json') as json_data:
    d = json.load(json_data)

    with open("Output.txt","w") as output:

        #File Header
        print(f"{{", file=output)
        print(f"\"Loop\": \"none\",", file=output)
        print(f"\"Frames\":", file=output)
        print(f"[", file=output)

        #Start of Keyframes
        numFrames = 30
        for i in range(0,numFrames):
            if i < (numFrames - 1):     # put comma at end of all arrays except last one (JSON format)
                ending = ","
            else:
                ending = ""
            quat = euler_to_quaternion(d["X"][(2*i)+1], d["Y"][(2*i)+1], d["Z"][(2*i)+1])
            print(f"[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,{quat[3]},{quat[0]},{quat[1]},{quat[2]},0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]{ending}", file=output)
            #print(f"[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,{w},{x},{y},{z},0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]", file=output)

        #Closing up file
        print(f"]", file=output)
        print(f"}}", file=output)