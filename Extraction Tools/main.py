'''
Creates All Feature Extraction Files
Author: John Dogan
'''

from extract import *
from filemaker import *
from seperateWalkandFall import *

'''
1. User Enters Raw File Location
2. All required files for training are created
'''
def main():

    #RAW FILE NEEDED FROM USER
    filename = input("RAW FILE - ENTER FILE LOCATION: ")

    #TIME BEFORE FALL OCCURS NEEDED FROM USER
    timeActivity = int(input("ENTER WHEN FALL OCCURS (In Seconds): "))

    #SEPERATE FALL AND BEFORE FALL
    seperate(filename, timeActivity)

    #CREATE BEFORE FALL AND AFTER FALL FILES
    for i in range(2):

        #Before Fall
        if(i == 0):

            filemaker("beforeFall.txt", "before_", filename)

        #After Fall
        else:

            filemaker("afterFall.txt", "after_", filename)

    #will create all features files from new filename
    for i in range(11):

        #FOR ALL BEFORE SENSOR FILES
        if(i < 6):

            new = "before_"

            #Write according to sensor
            if(i == 0):

                accBefore = extract(new + "accFile_" + filename)

                xAccBefore, yAccBefore, zAccBefore = accBefore.getAll()


            elif(i == 1):

                gravBefore = extract(new + "gravFile_" + filename)

                xGravBefore, yGravBefore, zGravBefore = gravBefore.getAll()

            elif(i == 2):

                gyroBefore = extract(new + "gyroFile_" + filename)

                xGyroBefore, yGyroBefore, zGyroBefore = gyroBefore.getAll()

            elif(i == 3):

                linearBefore = extract(new + "linearFile_" + filename)

                xLinearBefore, yLinearBefore, zLinearBefore = linearBefore.getAll()

            elif(i == 4):

                magBefore = extract(new + "magFile_" + filename)

                xMagBefore, yMagBefore, zMagBefore = magBefore.getAll()

        #FOR ALL AFTER SENSOR FILES
        else:

            #AFTER FALL
            new = "after_"

            # Write according to sensor
            if(i == 6):

                accAfter = extract(new + "accFile_" + filename)

                xAccAfter, yAccAfter, zAccAfter = accAfter.getAll()

            elif(i == 7):

                gravAfter = extract(new + "gravFile_" + filename)

                xGravAfter, yGravAfter, zGravAfter = gravAfter.getAll()

            elif(i == 8):

                 gyroAfter = extract(new + "gyroFile_" + filename)

                 xGyroAfter, yGyroAfter, zGyroAfter = gyroAfter.getAll()

            elif(i == 9):

                 linearAfter = extract(new + "linearFile_" + filename)

                 xLinearAfter, yLinearAfter, zLinearAfter = linearAfter.getAll()

            elif(i == 10):

                 magAfter = extract(new + "magFile_" + filename)

                 xMagAfter, yMagAfter, zMagAfter = magAfter.getAll()

    #FEATURE FILE TO WRITE FROM ANYWHERE
    # 1. MULTI
    #CREATING TRAINING
    featuresFileAcc = open("featureFileFilteredMultiAcc.txt", 'a')
    featuresFileGrav = open("featureFileFilteredMultiGrav.txt", 'a')
    featuresFileGyro = open("featureFileFilteredMultiGyro.txt", 'a')
    featuresFileLinear = open("featureFileFilteredMultiLinear.txt", 'a')
    featuresFileMag = open("featureFileFilteredMultiMag.txt", 'a')
    #CREATING TESt
    #featuresFileAcc = open("featureFileTestFilteredMultiAcc.txt", 'a')
    #featuresFileGrav = open("featureFileTestFilteredMultiGrav.txt", 'a')
    #featuresFileGyro = open("featureFileTestFilteredMultiGyro.txt", 'a')
    #featuresFileLinear = open("featureFileTestFilteredMultiLinear.txt", 'a')
    #featuresFileMag = open("featureFileTestFilteredMultiMag.txt", 'a')
    # 2. BINARY
    #CREATING TRAINING
    #featuresFileAcc = open("featureFileFilteredBinaryAccPocket.txt", 'a')
    #featuresFileGrav = open("featureFileFilteredBinaryGravPocket.txt", 'a')
    #featuresFileGyro = open("featureFileFilteredBinaryGyroPocket.txt", 'a')
    #featuresFileLinear = open("featureFileFilteredBinaryLinearPocket.txt", 'a')
    #featuresFileMag = open("featureFileFilteredBinaryMagPocket.txt", 'a')
    #CREATING TEST
    #featuresFileAcc = open("featureFileTestFilteredBinaryAccPocket.txt", 'a')
    #featuresFileGrav = open("featureFileTestFilteredBinaryGravPocket.txt", 'a')
    #featuresFileGyro = open("featureFileTestFilteredBinaryGyroPocket.txt", 'a')
    #featuresFileLinear = open("featureFileTestFilteredBinaryLinearPocket.txt", 'a')
    #featuresFileMag = open("featureFileTestFilteredBinaryMagPocket.txt", 'a')
    # 3. OTHERS
    #FINISH CREATING FILES FOR EACH SENSORS AXIS
    #CREATING TEST
    #featuresFileX = open("featureFileTestFilteredXAccMulti.txt", 'a')
    #featuresFileY = open("featureFileTestFilteredYAccMulti.txt", 'a')
    #featuresFileZ = open("featureFileTestFilteredZAccMulti.txt", 'a')
    # CREATING TRAINING
    # featuresFileX = open("featureFileFilteredXAccMulti.txt", 'a')
    # featuresFileY = open("featureFileFilteredYAccMulti.txt", 'a')
    # featuresFileZ = open("featureFileFilteredZAccMulti.txt", 'a')

    #EXTRACT ALL AXIS OR EACH INDIVIDUAL AXIS
    usrExtract = input("\nExtract all Axis (y/N): ")

    #CLASS FOR BEFORE
    cfBefore = input("\nEnter Classifier Before Fall: ")

    # CLASS FOR AFTER
    cfAfter = input("Enter Classifier After Fall: ")

    #IF ALL AXIS INCLUDED
    if(usrExtract.lower() == "y".lower()):

        #For ALL BEFORE FALL
        for i in range(len(xAccBefore)):
            for AccX in range(len(xAccBefore[i])):
                featuresFileAcc.write(xAccBefore[i][AccX] + " ")
            for AccY in range(len(yAccBefore[i])):
                featuresFileAcc.write(yAccBefore[i][AccY] + " ")
            for AccZ in range(len(zAccBefore[i])):
                featuresFileAcc.write(zAccBefore[i][AccZ] + " ")

            featuresFileAcc.write(cfBefore + "\n")

        for i in range(len(xGravBefore)):
            for GravX in range(len(xGravBefore[i])):
                featuresFileGrav.write(xGravBefore[i][GravX] + " ")
            for GravY in range(len(yGravBefore[i])):
                featuresFileGrav.write(yGravBefore[i][GravY] + " ")
            for GravZ in range(len(zGravBefore[i])):
                featuresFileGrav.write(zGravBefore[i][GravZ] + " ")

            featuresFileGrav.write(cfBefore + "\n")

        for i in range(len(xGyroBefore)):
            for GyroX in range(len(xGyroBefore[i])):
                featuresFileGyro.write(xGyroBefore[i][GyroX] + " ")
            for GyroY in range(len(yGyroBefore[i])):
                featuresFileGyro.write(yGyroBefore[i][GyroY] + " ")
            for GyroZ in range(len(zGyroBefore[i])):
                featuresFileGyro.write(zGyroBefore[i][GyroZ] + " ")

            featuresFileGyro.write(cfBefore + "\n")

        for i in range(len(xLinearBefore)):
            for LinearX in range(len(xLinearBefore[i])):
                featuresFileLinear.write(xLinearBefore[i][LinearX] + " ")
            for LinearY in range(len(yLinearBefore[i])):
                featuresFileLinear.write(yLinearBefore[i][LinearY] + " ")
            for LinearZ in range(len(zLinearBefore[i])):
                featuresFileLinear.write(zLinearBefore[i][LinearZ] + " ")

            featuresFileLinear.write(cfBefore + "\n")

        for i in range(len(xMagBefore)):
            for MagX in range(len(xMagBefore[i])):
                featuresFileMag.write(xMagBefore[i][MagX] + " ")
            for MagY in range(len(yMagBefore[i])):
                featuresFileMag.write(yMagBefore[i][MagY] + " ")
            for MagZ in range(len(zMagBefore[i])):
                featuresFileMag.write(zMagBefore[i][MagZ] + " ")

            featuresFileMag.write(cfBefore + "\n")

        # FOR ALL AFTER FALL
        for i in range(len(xAccAfter)):
            for AccX in range(len(xAccAfter[i])):
                featuresFileAcc.write(xAccAfter[i][AccX] + " ")
            for AccY in range(len(yAccAfter[i])):
                featuresFileAcc.write(yAccAfter[i][AccY] + " ")
            for AccZ in range(len(zAccAfter[i])):
                featuresFileAcc.write(zAccAfter[i][AccZ] + " ")

            featuresFileAcc.write(cfAfter + "\n")

        for i in range(len(xGravAfter)):
            for GravX in range(len(xGravAfter[i])):
                featuresFileGrav.write(xGravAfter[i][GravX] + " ")
            for GravY in range(len(yGravAfter[i])):
                featuresFileGrav.write(yGravAfter[i][GravY] + " ")
            for GravZ in range(len(zGravAfter[i])):
                featuresFileGrav.write(zGravAfter[i][GravZ] + " ")

            featuresFileGrav.write(cfAfter + "\n")

        for i in range(len(xGyroAfter)):
            for GyroX in range(len(xGyroAfter[i])):
                featuresFileGyro.write(xGyroAfter[i][GyroX] + " ")
            for GyroY in range(len(yGyroAfter[i])):
                featuresFileGyro.write(yGyroAfter[i][GyroY] + " ")
            for GyroZ in range(len(zGyroAfter[i])):
                featuresFileGyro.write(zGyroAfter[i][GyroZ] + " ")

            featuresFileGyro.write(cfAfter + "\n")

        for i in range(len(xLinearAfter)):
            for LinearX in range(len(xLinearAfter[i])):
                featuresFileLinear.write(xLinearAfter[i][LinearX] + " ")
            for LinearY in range(len(yLinearAfter[i])):
                featuresFileLinear.write(yLinearAfter[i][LinearY] + " ")
            for LinearZ in range(len(zLinearAfter[i])):
                featuresFileLinear.write(zLinearAfter[i][LinearZ] + " ")

            featuresFileLinear.write(cfAfter + "\n")

        for i in range(len(xMagAfter)):
            for MagX in range(len(xMagAfter[i])):
                featuresFileMag.write(xMagAfter[i][MagX] + " ")
            for MagY in range(len(yMagAfter[i])):
                featuresFileMag.write(yMagAfter[i][MagY] + " ")
            for MagZ in range(len(zMagAfter[i])):
                featuresFileMag.write(zMagAfter[i][MagZ] + " ")

            featuresFileMag.write(cfAfter + "\n")

        featuresFileAcc.close()
        featuresFileGrav.close()
        featuresFileGyro.close()
        featuresFileLinear.close()
        featuresFileMag.close()

    # IF ALL AXIS SEPERATE
    elif(usrExtract.lower() == "N".lower()):

        #For ALL BEFORE FALL
        for i in range(len(xAccBefore)):

            #TIMES 3 FOR 3 LISTS
            for j in range(len(xAccBefore[i])):

                featuresFileX.write(xAccBefore[i][j] + " ")

            for k in range(len(yAccBefore[i])):

                featuresFileY.write(yAccBefore[i][k] + " ")

            for m in range(len(zAccBefore[i])):

                featuresFileZ.write(zAccBefore[i][m] + " ")

            featuresFileX.write(cfBefore + "\n")
            featuresFileY.write(cfBefore + "\n")
            featuresFileZ.write(cfBefore + "\n")


        #FOR ALL AFTER FALL
        for i in range(len(xAccAfter)):

            #TIMES 3 FOR 3 LISTS
            for j in range(len(xAccAfter[i])):

                featuresFileX.write(xAccAfter[i][j] + " ")

            for k in range(len(yAccAfter[i])):

                featuresFileY.write(yAccAfter[i][k] + " ")

            for m in range(len(zAccAfter[i])):

                featuresFileZ.write(zAccAfter[i][m] + " ")

            featuresFileX.write(cfAfter + "\n")
            featuresFileY.write(cfAfter + "\n")
            featuresFileZ.write(cfAfter + "\n")

        featuresFileX.close()
        featuresFileY.close()
        featuresFileZ.close()

if __name__ == '__main__':
    main()



