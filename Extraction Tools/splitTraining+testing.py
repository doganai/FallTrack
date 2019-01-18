'''
Classification File
Author: John Dogan
1. Get File Name and Put features into list
2. Split Data into Desired Set
'''


from collections import Counter
import math

#MULTICLASS CLASSIFICATION
# Classes: 1 is Jog, 2 is JogFall, 3 is Walk, 4 is WalkFall, 5 is stand, 6 is standFall,
# 7 is sit, 8 is sitFall, 9 is lie, 10 is lieFall, 11 is stairUp,
# 12 is stairUpFall, 13 is stairDown, 14 is stairDownFall

'''
Retrieve file name, gather features for SVM, runSVM
'''
def main():

        featureFile = input("Enter Feature File: ")
        featureFile = open(featureFile, 'r')

        lines = featureFile.readlines()

        X, CF, size = gatherFeatures(lines)

        splitData(X,CF,size)


'''
Gather Features From BeforeFall And AfterFall files
'''
def gatherFeatures(lines):

    #MATCH THE X AND CLASS IN A LIST
    X = []
    CF = []

    # FEATURE FILE
    for line in lines:

        featuresLine = line.split()

        #MAKES SURE ALL FEATURE LINES ARE THE SAME SIZE
        if(46 == len(featuresLine)):

            cfLine = line.split()


            X.append(featuresLine[:-1])


            CF.append(cfLine[-1].replace("\n", " "))


    #SPLIT TRAINING + TESTING
    trainingSize = .60 #60% training

    count = Counter(CF)
    size = []
    size.append(math.ceil(count['1']*trainingSize))
    size.append(math.ceil(count['2']*trainingSize))
    size.append(math.ceil(count['3']*trainingSize))
    size.append(math.ceil(count['4']*trainingSize))
    size.append(math.ceil(count['5']*trainingSize))
    size.append(math.ceil(count['6']*trainingSize))
    size.append(math.ceil(count['7'] * trainingSize))
    size.append(math.ceil(count['8'] * trainingSize))
    size.append(math.ceil(count['9'] * trainingSize))
    size.append(math.ceil(count['10'] * trainingSize))
    size.append(math.ceil(count['11'] * trainingSize))
    size.append(math.ceil(count['12'] * trainingSize))
    size.append(math.ceil(count['13'] * trainingSize))
    size.append(math.ceil(count['14'] * trainingSize))



    return X, CF, size

'''
Split Data into Training and Testing
'''
def splitData(X,CF, size):

    trainingFile = open("MagTrainingFile.txt", 'w')
    testFile = open("MagTestingFile.txt", 'w')

    i = 0;
    count = [0] * 14;

    while i in range(len(X)):

        if(CF[i] == '1'):

            if(count[0] < size[0]):

                currentLine = str(X[i]).replace("'", "")
                currentLine = currentLine[1:-1] + ', ' + str(CF[i])
                trainingFile.write((currentLine) + '\n')

            else:

                currentLine = str(X[i]).replace("'", "")
                currentLine = currentLine[1:-1] + ', ' + str(CF[i])
                testFile.write((currentLine) + '\n')

            count[0] = count[0] + 1;

        if(CF[i] == '2'):

            if (count[1] < size[1]):

                currentLine = str(X[i]).replace("'", "")
                currentLine = currentLine[1:-1] + ', ' + str(CF[i])
                trainingFile.write((currentLine) + '\n')

            else:

                currentLine = str(X[i]).replace("'", "")
                currentLine = currentLine[1:-1] + ', ' + str(CF[i])
                testFile.write((currentLine) + '\n')

            count[1] = count[1] + 1;

        elif (CF[i] == '3'):

            if (count[2] < size[2]):

                currentLine = str(X[i]).replace("'", "")
                currentLine = currentLine[1:-1] + ', ' + str(CF[i])
                trainingFile.write((currentLine) + '\n')

            else:

                currentLine = str(X[i]).replace("'", "")
                currentLine = currentLine[1:-1] + ', ' + str(CF[i])
                testFile.write((currentLine) + '\n')

            count[2] = count[2] + 1;

        elif (CF[i] == '4'):

            if (count[3] < size[3]):

                currentLine = str(X[i]).replace("'", "")
                currentLine = currentLine[1:-1] + ', ' + str(CF[i])
                trainingFile.write((currentLine) + '\n')

            else:

                currentLine = str(X[i]).replace("'", "")
                currentLine = currentLine[1:-1] + ', ' + str(CF[i])
                testFile.write((currentLine) + '\n')

            count[3] = count[3] + 1;

        elif (CF[i] == '5'):

            if (count[4] < size[4]):

                currentLine = str(X[i]).replace("'", "")
                currentLine = currentLine[1:-1] + ', ' + str(CF[i])
                trainingFile.write((currentLine) + '\n')

            else:

                currentLine = str(X[i]).replace("'", "")
                currentLine = currentLine[1:-1] + ', ' + str(CF[i])
                testFile.write((currentLine) + '\n')

            count[4] = count[4] + 1;

        elif (CF[i] == '6'):

            if (count[5] < size[5]):

                currentLine = str(X[i]).replace("'", "")
                currentLine = currentLine[1:-1] + ', ' + str(CF[i])
                trainingFile.write((currentLine) + '\n')

            else:

                currentLine = str(X[i]).replace("'", "")
                currentLine = currentLine[1:-1] + ', ' + str(CF[i])
                testFile.write((currentLine) + '\n')

            count[5] = count[5] + 1;

        elif (CF[i] == '7'):

            if (count[6] < size[6]):

                currentLine = str(X[i]).replace("'", "")
                currentLine = currentLine[1:-1] + ', ' + str(CF[i])
                trainingFile.write((currentLine) + '\n')

            else:

                currentLine = str(X[i]).replace("'", "")
                currentLine = currentLine[1:-1] + ', ' + str(CF[i])
                testFile.write((currentLine) + '\n')

            count[6] = count[6] + 1;

        elif (CF[i] == '8'):

            if (count[7] < size[7]):

                currentLine = str(X[i]).replace("'", "")
                currentLine = currentLine[1:-1] + ', ' + str(CF[i])
                trainingFile.write((currentLine) + '\n')

            else:

                currentLine = str(X[i]).replace("'", "")
                currentLine = currentLine[1:-1] + ', ' + str(CF[i])
                testFile.write((currentLine) + '\n')

            count[7] = count[7] + 1;

        elif (CF[i] == '9'):

            print()

            if (count[8] < size[8]):

                currentLine = str(X[i]).replace("'", "")
                currentLine = currentLine[1:-1] + ', ' + str(CF[i])
                trainingFile.write((currentLine) + '\n')

            else:

                currentLine = str(X[i]).replace("'", "")
                currentLine = currentLine[1:-1] + ', ' + str(CF[i])
                testFile.write((currentLine) + '\n')

            count[8] = count[8] + 1;

        elif (CF[i] == '10'):

            if (count[9] < size[9]):

                currentLine = str(X[i]).replace("'", "")
                currentLine = currentLine[1:-1] + ', ' + str(CF[i])
                trainingFile.write((currentLine) + '\n')

            else:

                currentLine = str(X[i]).replace("'", "")
                currentLine = currentLine[1:-1] + ', ' + str(CF[i])
                testFile.write((currentLine) + '\n')

            count[9] = count[9] + 1;

        elif (CF[i] == '11'):

            if (count[10] < size[10]):

                currentLine = str(X[i]).replace("'", "")
                currentLine = currentLine[1:-1] + ',' + str(CF[i])
                trainingFile.write((currentLine) + '\n')

            else:

                currentLine = str(X[i]).replace("'", "")
                currentLine = currentLine[1:-1] + ', ' + str(CF[i])
                testFile.write((currentLine) + '\n')

            count[10] = count[10] + 1;

        elif (CF[i] == '12'):

            if (count[11] < size[11]):

                currentLine = str(X[i]).replace("'", "")
                currentLine = currentLine[1:-1] + ', ' + str(CF[i])
                trainingFile.write((currentLine) + '\n')

            else:

                currentLine = str(X[i]).replace("'", "")
                currentLine = currentLine[1:-1] + ', ' + str(CF[i])
                testFile.write((currentLine) + '\n')

            count[11] = count[11] + 1;

        elif (CF[i] == '13'):

            if (count[12] < size[12]):

                currentLine = str(X[i]).replace("'", "")
                currentLine = currentLine[1:-1] + ', ' + str(CF[i])
                trainingFile.write((currentLine) + '\n')

            else:

                currentLine = str(X[i]).replace("'", "")
                currentLine = currentLine[1:-1] + ', ' + str(CF[i])
                testFile.write((currentLine) + '\n')

            count[12] = count[12] + 1;

        elif (CF[i] == '14'):

            if (count[13] < size[13]):

                currentLine = str(X[i]).replace("'", "")
                currentLine = currentLine[1:-1] + ', ' + str(CF[i])
                trainingFile.write((currentLine) + '\n')

            else:

                currentLine = str(X[i]).replace("'", "")
                currentLine = currentLine[1:-1] + ', ' + str(CF[i])
                testFile.write((currentLine) + '\n')

            count[13] = count[13] + 1;

        i = i + 1;

    print(count)

if __name__ == '__main__':
    main()











