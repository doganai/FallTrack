'''
Author:
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

        count = 0

        # DISPLAY END MARK AND COUNT TILL END MARK
        for i in range(len(times) - 1):

            # Limit before setting the endMark for when fall occurs
            if (times[i] >= limitMark):

                endMark = times[i - 1]

                count = i

                break

        for i in range(len(times) - 1):

            # WRITE TO ALL BEFORE FALL
            if (i <= count - 1):

                fileBeforeFall.write(
                    str(times[i]) + " " + str(sensors[i]) + " " + str(x[i]) + " " + str(y[i]) + " " + str(z[i]) + "\n")

            # WRITE TO ALL AFTER FALL
            else:

                fileAfterFall.write(
                    str(times[i]) + " " + str(sensors[i]) + " " + str(x[i]) + " " + str(y[i]) + " " + str(z[i]) + "\n")

        print("EndMARK = " + str(endMark))
        fileBeforeFall.close()
        fileAfterFall.close()