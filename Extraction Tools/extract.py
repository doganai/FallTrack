'''
Author: John Dogan
Extract features from given sensor file for Android in format (time,sensor type,x,y,z)
Writes data like height, width, and distance up and down to a file.
Uses 50% window overlapping
Returns Features for the X, Y, and Z axis
'''

from collections import defaultdict
import numpy

class extract():

    '''
    Open sensor file and extract data from it and write information to new file
    '''

    allWindowFeaturesX = []
    allWindowFeaturesY = []
    allWindowFeaturesZ = []

    def __init__(self, filename):

        # Open Sensor File
        file = open(filename, 'r')

        # Read lines
        lines = file.readlines()

        # Seperated data
        time,x,y,z = self.seperateData(lines)

        # Features for X axis
        self.allWindowsFeaturesX = self.writeFeatures(time, x, "X_" + filename)

        # Features for Y axis
        self.allWindowsFeaturesY = self.writeFeatures(time, y, "Y_" + filename)

        # Features for Z axis
        self.allWindowsFeaturesZ = self.writeFeatures(time, z, "Z_" + filename)

    '''
    Return X,Y,Z features in file
    @return allWindowFeaturesX, all..Y, all..Z: Returns all X,Y,Z features in a list
    '''
    def getAll(self):

        return self.allWindowsFeaturesX, self.allWindowsFeaturesY, self.allWindowsFeaturesZ;

    '''
    Seperate data in data file
    @return time,x,y,z: Returns all separated data from given sensor file
    '''
    def seperateData(self, lines):

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
    def writeFeatures(self, time, axis, fileName):

        ###############################################################
        # 1. ORGANIZE DATA INTO WINDOWS
        ###############################################################

        #CREATE FILE TO WRITE IN
        #file = open(fileName , 'w')

        #File created to extract into
        #extractFile = open("features_" + fileName, 'w')
        #extractFile.write("UpPeak DownPeak Cycle MeanOfAllAxis SDofAllAxis RMSofAllAxis MinMaxofAllAxis ""HeightFeature WidthFeature MeanofCycleHeight MeanofCycleWidth MeanOfCycleDistance ""SDofCycleHeight SDofCycleWidth SDofCycleDistance ...\n")

        #DICT OF TIME AND AXIS ITEMS
        timeDict = defaultdict(list)
        axisDict = defaultdict(list)

        allWindowFeatures = [];
        features = []


        #POSITION OF PLACE IN WINDOW
        i = 0

        #NEW WINDOW
        window = 1
        windowStart = time[i]
        windowSize = 2000 #2 Seconds
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
        upPeak = []
        downPeak = []

        #ALL PEAKS IN WHOLE FILE
        upPeaks = 0
        downPeaks = 0

        #List Version
        listUpPeaks = [];
        listDownPeaks = [];

        #IS THIS A HALF CYCLE? TURNS TRUE WHEN IT REACHES A PEAK AND ENDS AT HIGHEST PEAK OR LOWEST PEAK
        cycles = 0
        cycle = False
        lastSign = ''

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
            #file.write("WINDOW: " + str(i) + "\n")
            #file.write("--------------------------------------------\n\n")

            #For range in current window
            for w in range(len(timeDict[i])):

                # WRITE PLACE IN WINDOW
                #file.write("- TIME: " + str(timeDict[i][w]) + " AXIS: " + str(axisDict[i][w]) + "\n\n")

                # FEATURE EXTRACTION FROM ALL DATA
                listAxis.append(axisDict[i][w])
                listTime.append(timeDict[i][w])

                # STATEMENT CREATED FOR DATA IN HALF CYCLES
                #IF NOT LAST IN WINDOW THEN COMPARE
                if(len(axisDict[i]) != w+1 ):

                    #FEATURE EXTRACTION ALL HALF CYCLE DATA
                    #IF DATA GOES DOWN
                    if(axisDict[i][w] > axisDict[i][w+1]):

                        #file.write("POSITION: DOWN\n\n")

                        # START OF CYCLE
                        if((lastSign == 'DOWN') & (cycle == False)):

                            cycle = True

                            # UP PEAK
                            upPeak.append(timeDict[i][w - 1])

                            startTime.append(timeDict[i][w - 1])
                            startAxis.append(axisDict[i][w - 1])

                        # END OF CYCLE ENDS IN
                        elif(((lastSign == "UP") & (cycle == True))):

                            cycle = False

                            cycles = cycles + 1

                            # UP PEAK
                            upPeak.append(timeDict[i][w])

                            endTime.append(timeDict[i][w])
                            endAxis.append(axisDict[i][w])

                        # NEW SIGN
                        lastSign = "DOWN"

                    #IF DATA GOES UP
                    elif(axisDict[i][w] < axisDict[i][w+1]):

                        #file.write("POSITION: UP\n\n")

                        #START OF CYCLE
                        if((lastSign == 'UP') & (cycle == False)):

                            # HALF CYCLE STARTS
                            cycle = True

                            # DOWN PEAK
                            downPeak.append(timeDict[i][w - 1])

                            startTime.append(timeDict[i][w - 1])
                            startAxis.append(axisDict[i][w - 1])

                        #END OF HALF CYCLE
                        elif((lastSign == "DOWN") & (cycle == True)):

                            #HALF CYCLE ENDS
                            cycle = False

                            cycles = cycles + 1

                            # DOWN PEAK
                            downPeak.append(timeDict[i][w])

                            endTime.append(timeDict[i][w])
                            endAxis.append(axisDict[i][w])

                        # NEW SIGN
                        lastSign = "UP"

                #IF STILL IN CYCLE AND WINDOW HAS ENDED.
                #THE START IS DELETED
                elif(cycle == True):

                    cycle = False

                    # Last start is removed from list
                    # No longer in half cycle
                    startTime.pop()
                    startAxis.pop()

            #REMOVE ALL SAME OCCURENCES
            upPeak = list(set(upPeak))
            downPeak = list(set(downPeak))

            #file.write("\n"+str(upPeak))
            #file.write("\n"+str(downPeak)+"\n")

            #WRITE UPS AND DOWNS EXTRACTED
            #file.write("UP PEAKS: " + str(len(upPeak)) + "\n")
            #file.write("DOWN PEAKS: " + str(len(downPeak)) + "\n")
            #file.write("HALF CYCLES: " + str(cycles) + "\n")

            #WRITE TO EXTRACT FILE
            #extractFile.write(str(len(upPeak)) + " " + str(len(downPeak)) + " " + str(cycles) + " ")

            features.append(str(len(upPeak)))
            features.append(str(len(downPeak)))
            features.append(str(cycles))

            #ADD UP PEAKS AND DOWNPEAKS INTO LIST FOR varAPF at the end
            listUpPeaks.append(len(upPeak))
            listDownPeaks.append(len(downPeak))

            #WRITE START AND ENDS
            #file.write("\nSTARTS: " + str(startTime) +"\n")
            #file.write("ENDS: " + str(endTime)+"\n")

            #####################################################################
            # 3. WRITE FEATURES HERE (WRITES WHILE LOOPING THROUGH EACH WINDOW)
            # USED TO WRITE AND EXTRACT FEATURES AND RESET DATA
            #####################################################################

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
                #file.write("\nHEIGHT [" + str(s+1) + "]: " + str(height) + "\n")
                #file.write("WIDTH [" + str(s+1) + "]: " + str(width) + "\n")
                #file.write("DISTANCE [" + str(s + 1) + "]: " + str(distance) + "\n")

            #file.write("\n")

            #ADD ALL IN LIST EXCEPT THE FIRST
            totalHeight = sum(listHeight[1:])

            #ADD ALL IN LIST EXCEPT THE LAST
            totalWidth = sum(listWidth[:-1])

            #HEIGHT AND WIDTH FEATURES
            if((len(listHeight)-1 > 0) & (len(listWidth)-1 > 0) ):

                #AVG OF HEIGHT AND WIDTH EXCLUDING THE GREATEST FOR HEIGHT AND THE LEAST FOR WIDTH
                avgHeight = totalHeight/(len(listHeight)-1)
                avgWidth = totalWidth/(len(listWidth)-1)

                #SUBTRACT AVERAGE FROM HIGHEST OF ALL
                featureHeight = listHeight[0] - avgHeight
                #SUBTRACT AVERAGE FROM THE LEAST WIDTH
                featureWidth = avgWidth - listWidth[-1]
            else:
                # SUBTRACT AVERAGE FROM HIGHEST OF ALL
                featureHeight = 0
                # SUBTRACT AVERAGE FROM THE LEAST WIDTH
                featureWidth = 0

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
            #file.write("MEAN OF ALL AXIS: " + str(meanAxis) + "\n\n")

            #file.write("SD OF ALL AXIS: " + str(sdAxis) + "\n\n")

            #file.write("RMS OF ALL AXIS: " + str(rmsAxis) + "\n\n")

            #file.write("MINMAX OF ALL AXIS: " + str(minMaxAxis) + "\n\n")

            #WRITE TO EXTRACT FILE
            #extractFile.write(str(meanAxis) + " " + str(sdAxis) + " " + str(rmsAxis) + " " +  str(minMaxAxis) + " ")

            features.append(str(meanAxis))
            features.append(str(sdAxis))
            features.append(str(rmsAxis))
            features.append(str(minMaxAxis))

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
                #file.write("HEIGHT FEATURE: " + str(featureHeight) + "\n")
                #file.write("WIDTH FEATURE: " + str(featureWidth) + "\n\n")

                #file.write("MEAN OF CYCLE HEIGHT: " + str(avgHeight) + "\n")
                #file.write("MEAN OF CYCLE WIDTH: " + str(avgWidth) + "\n")
                #file.write("MEAN OF CYCLE DISTANCE: " + str(avgDistance) + "\n\n")

                #file.write("SD OF CYCLE HEIGHT: " + str(sdHeight) + "\n")
                #file.write("SD OF CYCLE WIDTH: " + str(sdWidth) + "\n")
                #file.write("SD OF CYCLE DISTANCE: " + str(sdDistance) + "\n")

                #Write features to Extract
                #extractFile.write(str(featureHeight) + " " + str(featureWidth) + " " + str(avgHeight) + " " +
                                  ##str(avgWidth) + " " + str(avgDistance) + " " + str(sdHeight) + " " + str(sdWidth) +
                                  ##" " + str(sdDistance) + "\n")

                features.append(str(featureHeight))
                features.append(str(featureWidth))
                features.append(str(avgHeight))
                features.append(str(avgWidth))
                features.append(str(avgDistance))
                features.append(str(sdHeight))
                features.append(str(sdWidth))
                features.append(str(sdDistance))


            #file.write("\n")
            #file.write("--------------------------------------------\n")

            #ADD ALL PEAKS
            upPeaks = len(upPeak) + upPeaks
            downPeaks = len(downPeak) + downPeaks



            #RESET DATA COUNT FOR NEXT WINDOW
            allWindowFeatures.append(features)
            features = []
            upPeak = [];
            downPeak = [];
            lastSign = "";
            cycle = False;
            cycles = 0
            listHeight = []
            listWidth = []
            listDistance = []
            listAxis = []
            listTime = []

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
        varAPFUpPeak = numpy.std(listUpPeaks)
        varAPFDownPeak = numpy.std(listDownPeaks)

        #WRITE PEAK DATA
        #file.write("\nAPF OF UPPEAKS: " + str(apfUpPeak) + "\n")
        #file.write("APF OF DOWNPEAKS: " + str(apfDownPeak) + "\n")
        #file.write("\nVarAPF OF UPPEAKS: " + str(varAPFUpPeak) + "\n")
        #file.write("VarAPF OF DOWNPEAKS: " + str(varAPFDownPeak) + "\n\n")

        # CLOSE FILE
        #file.close()
        #extractFile.close()

        return allWindowFeatures;

