'''
Classification File
Author: John Dogan
1. Get File Name and Put features into list
2. Train Classifiers
3. Gather Results
'''

import numpy as np
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn import preprocessing
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import GaussianNB
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier

'''
Retrieve file name, gather features for Classifiers, Retrieve data from Classifiers
'''
def main():

        featureFile = open("featureFile.txt",'r')

        featureTestFile = open("featureFileTest.txt", 'r')

        lines = featureFile.readlines()

        linesTest = featureTestFile.readlines()

        #GATHER FEATURES AND CLASSES AND INSERT INTO FILE
        X, CF, TestCF, TestX = gatherFeatures(lines, linesTest)

        #NORMALIZE DATA AND RUN THROUGH Classifiers
        runClassifiers(X, TestX, TestCF, CF)

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
def runClassifiers(listX, listTestX, listTestCF, CF):

    #CLASS ARRAY, STORES ALL CLASSES
    cf = np.array(CF)
    cfTest = np.array(listTestCF)

    #Convert to Array
    X = np.array(listX)
    TestX = np.array(listTestX)

    # NORMALIZE DATA
    X = preprocessing.scale(X)
    TestX = preprocessing.scale(TestX)

    #SVM GATHER DATA
    rbf_svc = SVC(kernel='rbf', gamma=0.00001, C=1000).fit(X, cf)

    #K NEIGHBOR GATHER DATA
    knn = KNeighborsClassifier(n_neighbors=1).fit(X, cf)

    #NAIVE BAYES GATHER DATA
    gnb = GaussianNB().fit(X, cf)

    #DECISION TREE
    dTree = tree.DecisionTreeClassifier().fit(X, cf)

    #RANDOM FOREST
    rForest = RandomForestClassifier(n_estimators=15, max_depth=None).fit(X, cf)

    #PREDICT
    predictedSVC = rbf_svc.predict(TestX);
    predictedKNN = knn.predict(TestX);
    predictedBayes = gnb.predict(TestX);
    predictedTree = dTree.predict(TestX);
    predictedForest = rForest.predict(TestX);

    predictedSVC = np.array(predictedSVC)
    predictedKNN = np.array(predictedKNN)
    predictedBayes = np.array(predictedBayes);
    predictedTree = np.array(predictedTree);
    predictedForest = np.array(predictedForest);

    #SAVE RESULTS TO DATA.TXT
    data = open("data.txt", "w")

    #WRITE PREDICTED DATA
    data.write("PREDICTIONS FROM TEST DATA (SVC): \n" + str(predictedSVC) + "\n\n")
    data.write("PREDICTIONS FROM TEST DATA: (KNN)\n" + str(predictedKNN) + "\n\n")
    data.write("PREDICTIONS FROM TEST DATA: (Bayes)\n" + str(predictedBayes) + "\n\n")
    data.write("PREDICTIONS FROM TEST DATA: (Decision Tree)\n" + str(predictedTree) + "\n\n")
    data.write("PREDICTIONS FROM TEST DATA: (Random Forest)\n" + str(predictedForest) + "\n\n")

    #Confusion Matrix Table
    result = confusion_matrix(cfTest, predictedSVC)

    #WRITE CONFUSION MATRIX
    data.write("CONFUSION MATRIX (SVC): \n")
    data.write(str(result) + '\n\n\n\n')
    data.write(str(classification_report(listTestCF, predictedSVC)) + '\n')

    #WRITE CONFUSION MATRIX
    data.write("CONFUSION MATRIX: (KNN) \n")
    data.write(str(result) + '\n\n\n')
    data.write(str(classification_report(listTestCF, predictedKNN)) + '\n')

    #WRITE CONFUSION MATRIX
    data.write("CONFUSION MATRIX: (BAYES) \n")
    data.write(str(result) + '\n\n\n')
    data.write(str(classification_report(listTestCF, predictedBayes)) + '\n')

    #WRITE CONFUSION MATRIX
    data.write("CONFUSION MATRIX: (Decision Tree) \n")
    data.write(str(result) + '\n\n\n')
    data.write(str(classification_report(listTestCF, predictedTree)) + '\n')

    #WRITE CONFUSION MATRIX
    data.write("CONFUSION MATRIX: (Random Forest) \n")
    data.write(str(result) + '\n\n\n')
    data.write(str(classification_report(listTestCF, predictedForest)) + '\n')

    #ACCURACY
    accuracySVC = accuracy_score(cfTest, predictedSVC)
    accuracyKNN = accuracy_score(cfTest, predictedKNN)
    accuracyBayes = accuracy_score(cfTest, predictedBayes)
    accuracyTree = accuracy_score(cfTest, predictedTree)
    accuracyForest = accuracy_score(cfTest, predictedForest)


    #WRITE ACCURACY
    data.write("\nACCURACY SVC: " + str(accuracySVC) + "\n\n")
    data.write("\nACCURACY KNN: " + str(accuracyKNN) + "\n\n")
    data.write("\nACCURACY BAYES: " + str(accuracyBayes) + "\n\n")
    data.write("\nACCURACY DECISION TREE: " + str(accuracyTree) + "\n\n")
    data.write("\nACCURACY RANDOM FOREST: " + str(accuracyForest) + "\n\n")



main()











