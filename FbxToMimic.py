import numpy as np
import math
import json

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

#euler_Original = (np.random.random(3) * 1).tolist() # Generate random rotation angles for XYZ within the range [0, 360)

#euler_Original = [43.596, -69.205, 60.544]
 
# euler_Original = [0.761, -1.208, 1.057]
# quat = euler_to_quaternion(euler_Original[0], euler_Original[1], euler_Original[2]) # Convert to Quaternion
# newEulerRot = quaternion_to_euler(quat[0], quat[1], quat[2], quat[3]) #Convert the Quaternion to Euler angles

# print ("Euler: ")
# print (euler_Original)
# print ("quat: ")
# print (quat)
# print ("Final Euler: ")
# print (newEulerRot)

with open('./rThigh.json') as json_data:
    d = json.load(json_data)

    with open("Output.txt","w") as output:

        #File Header
        print(f"{{", file=output)
        print(f"\"Loop\": \"none\",", file=output)
        print(f"\"Frames\":", file=output)
        print(f"[", file=output)

        #Start of Keyframes
        numFrames = 900
        for i in range(0,numFrames):
            if i < (numFrames - 1):     # put comma at end of all arrays except last one (JSON format)
                ending = ","
            else:
                ending = ""
            quat = euler_to_quaternion(math.radians(d["X"][(2*i)+1]), math.radians(d["Y"][(2*i)+1]), math.radians(d["Z"][(2*i)+1]))
            #print(f"[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,{quat[3]},{quat[0]},{quat[1]},{quat[2]},0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]{ending}", file=output)

            print(f"[0.016666, 0.254329, 1.109693, 0.027481, -0.269159, 0.300407, 0.914427, 0.033652, 0.977585, 0.027517, 0.053675, -0.201714, 0.903554, 0.067610, 0.088587, -0.413728,{quat[3]},{quat[0]},{quat[1]},{quat[2]}, -1.704043, 0.959067, 0.068498, 0.123147, -0.245627, 0.807969, -0.554312, -0.084408, 0.181106, 0.787253, 0.829243, 0.189034, 0.167192, 0.498667, -0.662138, 0.964729, -0.229754, 0.084958, 0.096405, 0.513164, 0.645140, 0.008855, 0.566020, 1.537844]{ending}", file=output)

        #Closing up file
        print(f"]", file=output)
        print(f"}}", file=output)