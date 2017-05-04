class filemaker():

    def __init__(self, filename, new, create):

        ##### OPEN FILE MyAcc.txt ######
        file = open(filename, 'r')

        win = file.readlines()

        self.fileCreate(win,new,create)

    ###### CREATE FILE FOR SENSOR USED #######
    def fileCreate(self, win,new,filename):

        accFile = open(new+ "accFile_" + filename, 'w')
        gyroFile = open(new+ "gyroFile_" + filename, 'w')
        magFile = open(new+ "magFile_" + filename, 'w')
        gravFile = open(new+ "gravFile_" + filename, 'w')
        linearFile = open(new+ "linearFile_" + filename, 'w')
        vectorFile = open(new+ "vectorFile_" + filename, 'w')

        ##### FOR EVERY LINE IN LIST #####
        for line in win:

            if "ACCELEROMETER" in line:

                accFile.write(line)

            elif "GYROSCOPE" in line:

                gyroFile.write(line)

            elif "MAGNETIC_FIELD" in line:

                magFile.write(line)

            elif "GRAVITY" in line:

                gravFile.write(line)

            elif "LINEAR_ACCELERATION" in line:

                linearFile.write(line)

            elif "ROTATION_VECTOR" in line:

                vectorFile.write(line)