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
    for i in range(12):

        #FOR ALL BEFORE SENSOR FILES
        if(i < 6):

            new = "before_"

            #Write according to sensor
            if(i == 0):
                s = extract(new + "accFile_" + filename)
                xAccBefore, yAccBefore, zAccBefore = s.getAll()
            #elif(i == 1):
             #   extract(new + "gravFile_" + filename)
            #elif(i == 2):
            #    extract(new + "gyroFile_" + filename)
            #elif(i == 3):
            #    extract(new + "linearFile_" + filename)
            #elif(i == 4):
            #    extract(new + "magFile_" + filename)
            #elif(i == 5):
            #    extract(new + "vectorFile_" + filename)

        #FOR ALL AFTER SENSOR FILES
        else:

            #AFTER FALL
            new = "after_"

            # Write according to sensor
            if(i == 6):
                a = extract(new + "accFile_" + filename)
                xAccAfter, yAccAfter, zAccAfter = a.getAll()
            #elif(i == 7):
                #extract(new + "gravFile_" + filename)
            #elif(i == 8):
             #   extract(new + "gyroFile_" + filename)
            #elif(i == 9):
             #   extract(new + "linearFile_" + filename)
            #elif(i == 10):
             #   extract(new + "magFile_" + filename)
            #elif(i == 11):
             #   extract(new + "vectorFile_" + filename)

    #FEATURE FILE TO WRITE FROM ANYWHERE
    #CREATING TEST
    #featuresFile = open("featureFileTest.txt", 'a')
    #CREATING TRAINING
    featuresFile = open("featureFile.txt", 'a')

    # Classes: 1 is Jog, 2 is JogFall, 3 is Walk, 4 is WalkFall, 5 is stand, 6 is standFall,
    # 7 is sit, 8 is sitFall, 9 is lie, 10 is lieFall, 11 is stairUp,
    # 12 is stairUpFall, 13 is stairDown, 14 is stairDownFall

    #CLASS FOR BEFORE
    cfBefore = input("\nEnter Classifier Before Fall: ")

    #For ALL BEFORE FALL
    for i in range(len(xAccBefore)):

        #TIMES 3 FOR 3 LISTS
        for j in range(len(xAccBefore[i])):

            featuresFile.write(xAccBefore[i][j] + " ")

        for k in range(len(yAccBefore[i])):

            featuresFile.write(yAccBefore[i][k] + " ")

        for m in range(len(zAccBefore[i])):

            featuresFile.write(zAccBefore[i][m] + " ")


        featuresFile.write(cfBefore + "\n")


    #CLASS FOR AFTER
    cfAfter = input("Enter Classifier After Fall: ")

    #FOR ALL AFTER FALL
    for i in range(len(xAccAfter)):

        #TIMES 3 FOR 3 LISTS
        for j in range(len(xAccAfter[i])):

            featuresFile.write(xAccAfter[i][j] + " ")

        for k in range(len(yAccAfter[i])):

            featuresFile.write(yAccAfter[i][k] + " ")

        for m in range(len(zAccAfter[i])):

            featuresFile.write(zAccAfter[i][m] + " ")

        featuresFile.write(cfAfter + "\n")

    featuresFile.close()

if __name__ == '__main__':
    main()



