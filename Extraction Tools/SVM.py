'''
Support Vector Machine
Author: John Dogan
1. Get File Name and Put features into list
2. Train SVM
3. Gather Results
'''

import numpy as np
from sklearn.svm import SVC
from sklearn import preprocessing
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score

'''
Retrieve file name, gather features for SVM, runSVM
'''
def main():

        featureFile = open("featureFile.txt",'r')

        featureTestFile = open("featureFileTest.txt", 'r')

        lines = featureFile.readlines()

        linesTest = featureTestFile.readlines()

        #GATHER FEATURES AND CLASSES AND INSERT INTO FILE
        X, CF, TestCF, TestX = gatherFeatures(lines, linesTest)

        #NORMALIZE DATA AND RUN THROUGH SVM OBJECT
        runSVM(X, TestX, TestCF, CF)

'''
Gather Features From BeforeFall And AfterFall files
'''
def gatherFeatures(lines, linesTest):

    #MATCH THE X AND CLASS IN A LIST
    X = []
    TestX = []
    CF = []
    TestCF = []

    # TRAINING FILE
    for line in lines:

        featuresLine = line.split()

        #MAKES SURE ALL FEATURE LINES ARE THE SAME SIZE
        if(46 == len(featuresLine)):

            X.append(featuresLine[:-1])

            cfLine = line.split()

            CF.append(cfLine[-1].replace("\n", " "))

    # TEST FILE
    for lineTest in linesTest:

        featuresLine = lineTest.split()

        if(46 == len(featuresLine)):

            TestX.append(featuresLine[:-1])

            cfLine = lineTest.split()

            TestCF.append(cfLine[-1].replace("\n", " "))



    return X, CF, TestCF, TestX;

'''
Run svm with given features
'''
def runSVM(listX, listTestX, listTestCF, CF):

    #CLASS ARRAY, STORES ALL CLASSES
    cf = np.array(CF)
    cfTest = np.array(listTestCF)

    #Convert to Array
    X = np.array(listX)
    TestX = np.array(listTestX)

    # NORMALIZE DATA
    X = preprocessing.scale(X)
    TestX = preprocessing.scale(TestX)

    predicted = []

    rbf_svc = SVC(kernel='rbf', gamma=0.00001, C=1000).fit(X, cf)

    for i in range(len(TestX)):

        predicted.append(rbf_svc.predict(TestX[i]));

    predicted = np.array(predicted)

    #SAVE RESULTS TO DATA.TXT
    data = open("data.txt", "w")

    #WRITE PREDICTED DATA
    data.write("PREDICTIONS FROM TEST DATA: \n" + str(predicted) + "\n\n")

    #Confusion Matrix Table
    result = confusion_matrix(cfTest, predicted)

    #WRITE CONFUSION MATRIX
    data.write("CONFUSION MATRIX:\n")
    data.write(str(result) + '\n\n\n')
    data.write(str(classification_report(listTestCF, predicted)))

    #ACCURACY
    accuracy = accuracy_score(cfTest, predicted)

    #WRITE ACCURACY
    data.write("\nACCURACY: " + str(accuracy) + "\n\n")


main()











