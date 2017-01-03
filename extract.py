'''
Author: John Dogan
Extract features from given sensor file for Android in format (time,sensor type,x,y,z)
Writes data like height, width, and distance up and down to a file.
Uses 50% window overlapping
'''

from collections import defaultdict

'''
Open sensor file and extract data from it and write information to new file
'''
def main():

    # Open Sensor File
    file = open('accFile.txt', 'r')

    # Read lines
    lines = file.readlines()

    # Seperated data
    time,x,y,z = seperateData(lines)

    # Features for X axis
    writeFeatures(time, x, "featuresX.txt")

    # Features for Y axis
    writeFeatures(time, y, "featuresY.txt")

    # Features for Z axis
    writeFeatures(time, z, "featuresZ.txt")

'''
Seperate data in data file
@return time,x,y,z: Returns all separated data from given sensor file
'''
def seperateData(lines):

    #DECLARE X,Y,Z, and Time
    time = []
    x = []
    y = []
    z = []

    #GET ALL TIMES AND X,Y,Z separately
    for line in lines:

        temp = line.split()

        time.append(int(temp[0]))

        x.append(float(temp[2]))

        y.append(float(temp[3]))

        z.append(float(temp[4]))

    return time,x,y,z;

'''
Write features to new file
1. ORGANIZE DATA INTO WINDOWS
2. EXTRACT FEATURES
3. WRITE FEAUTRES
'''
def writeFeatures(time, axis, fileName):

    ###############################################################
    # 1. ORGANIZE DATA INTO WINDOWS
    ###############################################################

    #CREATE FILE TO WRITE IN
    file = open(fileName , 'w')

    #DICT OF TIME AND AXIS ITEMS
    timeDict = defaultdict(list)
    axisDict = defaultdict(list)

    #POSITION OF PLACE IN WINDOW
    i = 0

    #NEW WINDOW
    window = 1
    windowStart = time[i]
    windowSize = 1000
    gotAlready = False
    nextWindowStartPosition = i

    #CREATE WINDOWS AND APPEND TO LIST
    while i in range(len(time)):

        #NEXT WINDOW
        if(time[i] > windowStart+windowSize):

            window = 1 + window

            #file.write("\n\nWINDOW: " + str(window) + "\n ------------------------")

            i = nextWindowStartPosition

            windowStart = windowStart+(windowSize/2)

            gotAlready = False

            continue

        #IF LARGER THAN HALF, SET NEW WINDOW 50% overlapping windows
        if ((time[i] > windowStart + windowSize / 2) & (gotAlready == False)):

            nextWindowStartPosition = i

            gotAlready = True

        #WRITE DATA TO FILE
        #file.write("\nTIME: " + str(time[i]) +  " AXIS: " + str(axis[i]))

        #APPEND TIME AND AXIS TO KEY WINDOW
        timeDict[window].append(time[i])
        axisDict[window].append(axis[i])

        #MOVE UP IN WINDOW
        i = 1 + i


    ###############################################################
    # 2. EXTRACT FEATURES HERE!
    # Use timeDict and axisDict to compare items
    ###############################################################

    #Overall Dict
    i = 1

    #upCount and downCount for Up and Down in Data
    upCount = 0
    downCount = 0

    #IS THIS A CYCLE? TURNS TRUE WHEN IT REACHES A PEAK AND ENDS AT HIGHEST PEAK OR LOWEST PEAK
    cycle = False
    lastSign = ''

    #TIME VALUES
    startTime = []
    endTime = []

    #AXIS VALUES
    startAxis = []
    endAxis = []

    #FEATURES
    height = 0
    width = 0
    distance = 0

    #WRITE ALL UP AND DOWNS IN WINDOW AND WRITE/EXTRACT FEATURES
    while i in range(len(timeDict)+1):

        #WINDOW NUMBER
        file.write("WINDOW: " + str(i) + "\n")
        file.write("--------------------------------------------\n\n")

        #For range in current window
        for w in range(len(timeDict[i])):

            # WRITE PLACE IN WINDOW
            file.write("- TIME: " + str(timeDict[i][w]) + " AXIS: " + str(axisDict[i][w]) + "\n\n")

            #IF NOT LAST IN WINDOW THEN COMPARE
            if(len(axisDict[i]) != w+1 ):

                #IF DATA GOES DOWN
                if(axisDict[i][w] > axisDict[i][w+1]):

                    file.write("POSITION: DOWN\n\n")

                    downCount = 1 + downCount

                    #COUNT PEAK
                    # START OF CYCLE
                    if((lastSign == 'DOWN') & (cycle == False)):

                        cycle = True

                        startTime.append(timeDict[i][w - 1])
                        startAxis.append(axisDict[i][w - 1])

                    # END OF CYCLE
                    elif(((lastSign == "UP") & (cycle == True))):

                        cycle = False

                        endTime.append(timeDict[i][w])
                        endAxis.append(axisDict[i][w])

                    # NEW SIGN
                    lastSign = "DOWN"

                #IF DATA GOES UP
                elif(axisDict[i][w] < axisDict[i][w+1]):

                    file.write("POSITION: UP\n\n")

                    #NUMBER OF UPS
                    upCount = 1 + upCount

                    #COUNT PEAK
                    #START OF CYCLE
                    if((lastSign == 'UP') & (cycle == False)):

                        cycle = True

                        startTime.append(timeDict[i][w - 1])
                        startAxis.append(axisDict[i][w - 1])

                    #END OF CYCLE
                    elif((lastSign == "DOWN") & (cycle == True)):

                        cycle = False

                        endTime.append(timeDict[i][w])
                        endAxis.append(axisDict[i][w])

                    # NEW SIGN
                    lastSign = "UP"

            #IF STILL IN CYCLE AND WINDOW HAS ENDED.
            #LAST POINT BECOMES END
            elif(cycle == True):

                cycle = False

                endTime.append(timeDict[i][w])
                endAxis.append(axisDict[i][w])

                file.write("\n")

        #WRITE UPS AND DOWNS EXTRACTED
        file.write("UPS: " + str(upCount) + "\n")
        file.write("DOWNS: " + str(downCount) + "\n")

        #WRITE START AND ENDS
        file.write("\nSTARTS: " + str(startTime) +"\n")
        file.write("ENDS: " + str(endTime)+"\n")

        #####################################################################
        # 3. WRITE FEATURES HERE (WRITES WHILE LOOPING THROUGH EACH WINDOW)
        # USED TO WRITE AND EXTRACT FEATURES AND RESET DATA
        #####################################################################

        #FOR NUMBER OF CYCLES IN WINDOW
        for s in range(len(startTime)):

            #EXTRACT HEIGHT
            height = abs(startAxis[s] - endAxis[s])

            #EXTRACT WIDTH
            width = endTime[s] - startTime[s]

            #EXTRACT DISTANCE
            distance = ((height**2) + (width**2)) ** .5

            #WRITE FEATURES
            file.write("\nHEIGHT [" + str(s+1) + "]: " + str(height) + "\n")
            file.write("WIDTH [" + str(s+1) + "]: " + str(width) + "\n")
            file.write("DISTANCE [" + str(s + 1) + "]: " + str(distance) + "\n")

        file.write("--------------------------------------------\n")

        #RESET DATA COUNT FOR NEXT WINDOW
        upCount = 0;
        downCount = 0;
        lastSign = ""
        cycle = False
        height = 0;
        width = 0;
        distance = 0;

        #RESET START AND END TIME VALUES
        startTime = []
        endTime = []

        #RESET START AND END AXIS VALUES
        startAxis = []
        endAxis = []

        #NEXT WINDOW IN DICTIONARY
        i = i + 1;

    #CLOSE FILE
    file.close()

main()
