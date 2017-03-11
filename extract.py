'''
Author: John Dogan
Extract features from given sensor file for Android in format (time,sensor type,x,y,z)
Writes data like height, width, and distance up and down to a file.
Uses 50% window overlapping
'''

from collections import defaultdict
import numpy

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
3. WRITE FEATURES AND EXTRACT FROM HALF CYCLES
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
    windowSize = 2000
    gotAlready = False
    nextWindowStartPosition = i

    #CREATE WINDOWS AND APPEND TO LIST
    while i in range(len(time)):

        #NEXT WINDOW
        if(time[i] > windowStart+windowSize):

            window = 1 + window

            i = nextWindowStartPosition

            windowStart = windowStart+(windowSize/2)

            gotAlready = False

            continue

        #IF LARGER THAN HALF, SET NEW WINDOW 50% overlapping windows
        if ((time[i] > windowStart + windowSize / 2) & (gotAlready == False)):

            nextWindowStartPosition = i

            gotAlready = True

        #APPEND TIME AND AXIS TO KEY WINDOW
        timeDict[window].append(time[i])
        axisDict[window].append(axis[i])

        #MOVE UP IN WINDOW
        i = 1 + i

    ###############################################################
    # 2. EXTRACT FEATURES HERE! THIS PART HANDLES PEAKS
    # Use timeDict and axisDict to compare items
    ###############################################################

    #Overall Dict
    i = 1

    #COUNT Peaks in DATA
    upPeak = 0
    downPeak = 0

    #ALL PEAKS IN WHOLE FILE
    upPeaks = 0
    downPeaks = 0
    upPeaksList = []
    downPeaksList = []

    #IS THIS A HALF CYCLE? TURNS TRUE WHEN IT REACHES A PEAK AND ENDS AT HIGHEST PEAK OR LOWEST PEAK
    lastSign = ''

    #STORES ALL VALUES
    allValues = []
    values = []

    #TIME VALUES
    startTime = []
    endTime = []

    #AXIS VALUES
    startAxis = []
    endAxis = []

    #FEATURES FOR CYCLE
    listHeight = []
    listWidth = []
    listDistance = []

    #FOR ALL AXIS AND TIME IN WINDOW
    listAxis = []
    listTime = []

    #WRITE ALL UP AND DOWNS IN WINDOW AND WRITE/EXTRACT FEATURES
    while i in range(len(timeDict)+1):

        #WINDOW NUMBER
        file.write("WINDOW: " + str(i) + "\n")
        file.write("--------------------------------------------\n\n")

        #For range in current window
        for w in range(len(timeDict[i])):

            # WRITE PLACE IN WINDOW
            file.write("- TIME: " + str(timeDict[i][w]) + " AXIS: " + str(axisDict[i][w]) + "\n\n")

            # FEATURE EXTRACTION FROM ALL DATA
            listAxis.append(axisDict[i][w])
            listTime.append(timeDict[i][w])

            # IF FIRST IN WINDOW
            if(w == 0):

                # GOES UP
                if(axisDict[i][w+1] >= axisDict[i][w]):

                    file.write("POSITION: UP\n\n")

                    lastSign = "UP"

                # GOES DOWN
                elif(axisDict[i][w+1] < axisDict[i][w]):

                    file.write("POSITION: DOWN\n\n")

                    lastSign = "DOWN"


            # NOT LAST IN WINDOW AND NOT FIRST IN WINDOW
            elif((w != 0) & (w != len(timeDict[i])-1)):

                # GOES UP
                if(axisDict[i][w+1] > axisDict[i][w]):

                    file.write("POSITION: UP\n\n")

                    if(lastSign == "DOWN"):

                        lastSign = "UP"

                        downPeak = downPeak + 1

                        # VALUES FOR LiSt
                        values.append(timeDict[i][w])
                        values.append(axisDict[i][w])
                        values.append("downPeak")

                        # APPEND ALL ITEMS IN WINDOW
                        allValues.append(values)

                # GOES DOWN
                elif(axisDict[i][w+1] < axisDict[i][w]):

                    file.write("POSITION: DOWN\n\n")

                    if(lastSign == "UP"):

                        lastSign = "DOWN"

                        upPeak = upPeak + 1

                        values.append(timeDict[i][w])
                        values.append(axisDict[i][w])
                        values.append("upPeak")

                        # APPEND ALL ITEMS IN WINDOW
                        allValues.append(values)

            #CLEAN VALUES
            values = []

        #WRITE UPS AND DOWNS EXTRACTED
        file.write("UP PEAKS: " + str(upPeak) + "\n")
        file.write("DOWN PEAKS: " + str(downPeak) + "\n")
        #INSERT INTO LIST
        upPeaksList.append(upPeak)
        downPeaksList.append(downPeak)

        #####################################################################
        # 3. WRITE FEATURES HERE (WRITES WHILE LOOPING THROUGH EACH WINDOW)
        # USED TO WRITE AND EXTRACT FEATURES AND RESET DATA
        #####################################################################

        #RETREIVE START AND END TIMES
        for r in range(len(allValues)-1):

            startTime.append(int(allValues[r][0]))
            startAxis.append(float(allValues[r][1]))
            endTime.append(int(allValues[r+1][0]))
            endAxis.append(float(allValues[r+1][1]))

        #WRITE START AND ENDS
        file.write("\nSTARTS: " + str(startTime) +"\n")
        file.write("ENDS: " + str(endTime)+"\n")
        file.write("HALF CYCLES: " + str(len(endTime)) + "\n")

        #FOR NUMBER OF HALF CYCLES IN WINDOW EXTRACT BASIC FEATURES
        for s in range(len(startTime)):

            #EXTRACT HEIGHT
            height = abs(startAxis[s] - endAxis[s])

            #GREATEST IS IN FRONT OF LIST
            if((len(listHeight) > 0)):

                if(listHeight[0] < height):

                    listHeight.insert(0, height)

                elif(listHeight[0] > height):

                    listHeight.append(height)

            else:

                listHeight.append(height)

            #EXTRACT WIDTH
            width = endTime[s] - startTime[s]

            # GREATEST IS IN FRONT OF LIST
            if(len(listWidth) > 0):

                if((listWidth[0] < width)):

                    listWidth.insert(0, width)

                elif ((listWidth[0] > width)):

                    listWidth.append(width)

            else:

                listWidth.append(width)

            #EXTRACT DISTANCE
            distance = ((height**2) + (width**2)) ** .5
            listDistance.append(distance)

            #WRITE FEATURES
            file.write("\nHEIGHT [" + str(s+1) + "]: " + str(height) + "\n")
            file.write("WIDTH [" + str(s+1) + "]: " + str(width) + "\n")
            file.write("DISTANCE [" + str(s + 1) + "]: " + str(distance) + "\n")

        file.write("\n")

        #ADD ALL IN LIST EXCEPT THE FIRST
        totalHeight = sum(listHeight[1:])

        #ADD ALL IN LIST EXCEPT THE LAST
        totalWidth = sum(listWidth[:-1])

        #HEIGHT AND WIDTH FEATURES
        if((len(listHeight) > 0) & (len(listWidth) > 0)):

            #AVG OF HEIGHT AND WIDTH EXCLUDING THE GREATEST FOR HEIGHT AND THE LEAST FOR WIDTH
            avgHeight = totalHeight/(len(listHeight))
            avgWidth = totalWidth/(len(listWidth))

            #SUBTRACT AVERAGE FROM HIGHEST OF ALL
            featureHeight = listHeight[0] - avgHeight
            #SUBTRACT AVERAGE FROM THE LEAST WIDTH
            featureWidth = avgWidth - listWidth[-1]

        # -ALL IN WINDOW
        # MEAN FOR ALL DATA
        meanAxis = numpy.mean(listAxis)

        # SD FOR ALL DATA
        sdAxis = numpy.std(listAxis)

        # RMS FOR ALL DATA
        rmsAxis = numpy.sqrt(numpy.mean(numpy.square(listAxis)))

        # MINMAX FOR ALL DATA
        # ORGANIZE FROM LEAST TO GREATEST USING QUICKSORT
        listAxis = numpy.sort(listAxis, kind='quicksort')
        minMaxAxis = abs(listAxis[0] - listAxis[-1])

        # THIS IS DATA COLLECTED FROM ALL CYCLES
        file.write("MEAN OF ALL AXIS: " + str(meanAxis) + "\n\n")

        file.write("SD OF ALL AXIS: " + str(sdAxis) + "\n\n")

        file.write("RMS OF ALL AXIS: " + str(rmsAxis) + "\n\n")

        file.write("MINMAX OF ALL AXIS: " + str(minMaxAxis) + "\n\n")

        # DATA IN HALF CYCLES
        # LIST MUST BE BIGGER THAN 0
        if(len(listHeight) > 0):

            # -ALL IN CYCLE
            #ADD CYCLE HEIGHT
            cycleHeight = sum(listHeight)
            cycleWidth = sum(listWidth)
            cycleDistance = sum(listDistance)

            # GET THE MEAN OF THE VALUES
            avgHeight = cycleHeight / len(listHeight)
            avgWidth = cycleWidth / len(listWidth)
            # avgDistance is made for further distance analysis
            avgDistance = cycleDistance / len(listDistance)

            # GET SD OF THE VALUES
            sdHeight = numpy.std(listHeight)
            sdWidth = numpy.std(listWidth)
            sdDistance = numpy.std(listDistance)

            #CONTINUE WRITING FEATURES AT END OF HALF CYCLE
            file.write("HEIGHT FEATURE: " + str(featureHeight) + "\n")
            file.write("WIDTH FEATURE: " + str(featureWidth) + "\n\n")

            file.write("MEAN OF CYCLE HEIGHT: " + str(avgHeight) + "\n")
            file.write("MEAN OF CYCLE WIDTH: " + str(avgWidth) + "\n")
            file.write("MEAN OF CYCLE DISTANCE: " + str(avgDistance) + "\n\n")

            file.write("SD OF CYCLE HEIGHT: " + str(sdHeight) + "\n")
            file.write("SD OF CYCLE WIDTH: " + str(sdWidth) + "\n")
            file.write("SD OF CYCLE DISTANCE: " + str(sdDistance) + "\n")

        file.write("\n")
        file.write("--------------------------------------------\n")

        #ADD ALL PEAKS
        upPeaks =  upPeak + upPeaks
        downPeaks = downPeak + downPeaks

        #RESET DATA COUNT FOR NEXT WINDOW
        upPeak = 0;
        downPeak = 0;
        lastSign = "";
        listHeight = []
        listWidth = []
        listDistance = []
        listAxis = []
        listTime = []
        allValues = []

        #RESET START AND END TIME VALUES
        startTime = []
        endTime = []

        #RESET START AND END AXIS VALUES
        startAxis = []
        endAxis = []

        #NEXT WINDOW IN DICTIONARY
        i = i + 1;

    #NUMBER OF WINDOWS
    windows = i-1

    #APF
    apfUpPeak =  upPeaks/windows
    apfDownPeak = downPeaks/windows

    #varAPF
    stdAPFUpPeak = numpy.std(upPeaksList)
    stdAPFDownPeak = numpy.std(downPeaksList)

    #WRITE PEAK DATA
    file.write("\nAPF OF UPPEAKS: " + str(apfUpPeak) + "\n")
    file.write("APF OF DOWNPEAKS: " + str(apfDownPeak) + "\n")
    file.write("\nSTD APF OF UPPEAKS: " + str(stdAPFUpPeak) + "\n")
    file.write("STD APF OF DOWNPEAKS: " + str(stdAPFDownPeak) + "\n\n")

    #CLOSE FILE
    file.close()

main();
