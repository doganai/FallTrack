'''
Author: John Dogan
Seperate Activity and Fall Data from Raw File Given the time
'''
class seperate():

    def __init__(self, filename, timeActivity):

        ##### OPEN FILE RAW DATA FILE.txt ######
        file = open(filename, 'r')

        lines = file.readlines()

        # Amount of time before fall
        time = timeActivity*1000;  # 1000 = 1s

        # Seperate All Lines into a list
        sensors, times, x, y, z = self.seperateData(lines);

        # Analyze And Write All Data to seperate files
        self.analyzeAndWrite(sensors, time, times, x, y, z);

    '''
    Seperates the walk and fall to seperate files with given time from user
    '''
    def seperateData(self,lines):

        ##STORE ALL X Y Z
        x = []
        y = []
        z = []
        sensors = []

        ### All Times inserted into List
        times = [];

        # GET ALL TIMES
        for line in lines:

            temp = line.split()

            # Skip Blank Lines
            if (len(temp) > 0):
                times.append(int(temp[0]))

                sensors.append(str(temp[1]))

                x.append(float(temp[2]))

                y.append(float(temp[3]))

                z.append(float(temp[4]))

        return sensors, times, x, y, z

    def analyzeAndWrite(self, sensors, time, times, x, y, z):

        fileBeforeFall = open("beforeFall.txt", "w")
        fileAfterFall = open("afterFall.txt", "w")

        # When Fall Occurs
        limitMark = times[0] + time

        #FILTERING
        #REMOVE FIRST SECOND OF DATA
        removeFirstSecond = times[0] + 1000; #FIRST TIMESTAMP + 1000
        #REMOVE TIME OF FALL DATE
        removeAfterFall = .5 #.5 seconds
        #REMOVE ALL DATA NOT NEEDED AFTER FALL
        removeAllAfterFall = 1500 #1.5 seconds

        #ALL COUNTS FOR DATA
        count = 0
        startCount = 0
        removeFallCount = 0
        fallCount = 0

        # DISPLAY END MARK AND COUNT TILL END MARK
        for i in range(len(times) - 1):

            # Limit before setting the endMark for when fall occurs
            if (times[i] >= limitMark and count == 0):

                endMark = times[i]

                #REMOVE .5 SECOND AFTER FALL (FOR FILTERING)
                removeAfterFall = endMark + removeAfterFall;

                count = i

            # Limit to start t seconds after pressing start button mark (FOR FILTERING)
            elif(times[i] >= removeFirstSecond and startCount == 0):

                startCount = i

            # After Fall Filtering For t seconds after fall (FOR FILTERING)
            elif(times[i] >= removeAfterFall and fallCount == 0 and count != 0 and startCount != 0):

                fallCount = i

                removeAllAfterFall = times[i] + removeAllAfterFall

            # For data after fall that needs to be removed (FOR FILTERING)
            elif(times[i] >= removeAllAfterFall and removeFallCount == 0 and fallCount != 0):

                removeFallCount = i

        #START AFTER 1 SECOND
        j = startCount

        while j in range(len(times) - 1):

            # WRITE TO ALL BEFORE FALL
            if (j <= count - 1):

                fileBeforeFall.write(
                    str(times[j]) + " " + str(sensors[j]) + " " + str(x[j]) + " " + str(y[j]) + " " + str(z[j]) + "\n")

            # WRITE TO ALL AFTER FALL
            #j is between where fall is filtered and before the rest of the data is cutoff
            elif(j >= fallCount and j <= removeFallCount-1):

                fileAfterFall.write(
                    str(times[j]) + " " + str(sensors[j]) + " " + str(x[j]) + " " + str(y[j]) + " " + str(z[j]) + "\n")

            j = j + 1

        fileBeforeFall.close()
        fileAfterFall.close()