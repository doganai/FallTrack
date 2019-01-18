'''
Author: John Dogan
Creates graph from raw sensor data.
Shows user where to cut fall and non fall
'''

import matplotlib.pyplot as plt
from filemaker import *

'''
Graphs user data using matplotlib
Enter raw unseperated data then give a sensor file which comes from the raw file 
Make sure to refresh directory if needed
'''
def main():



    # RAW FILE NEEDED FROM USER
    filename = input("RAW FILE - ENTER FILE LOCATION TO GRAPH: ")
    filemaker(filename,"","")

    #RAW FILE NEEDED FROM USER (READS ACCELEROMETER SENSOR)
    filename = "accFile_"

    file = open(filename, "r")

    lines = file.readlines()

    #GATHER ALL DATA TO LIST
    times, x, y, z = seperateData(lines)

    x, = plt.plot(times, x, label="X")

    y, = plt.plot(times, y,label="Y")

    z, = plt.plot(times, z,label="Z")

    plt.legend([x,y,z],['X','Y','Z'])

    plt.show()

'''
Seperates data from file
@return x,y,z: Returns x,y,z
'''
def seperateData(lines):

    ##STORE ALL X Y Z
    x = []
    y = []
    z = []

    ### All Times inserted into List
    times = [];

    # GET ALL TIMES
    for line in lines:

        temp = line.split()

        # Skip Blank Lines
        if (len(temp) > 0):

            times.append(int(temp[0]))

            x.append(float(temp[2]))

            y.append(float(temp[3]))

            z.append(float(temp[4]))

    return times, x, y, z

main()