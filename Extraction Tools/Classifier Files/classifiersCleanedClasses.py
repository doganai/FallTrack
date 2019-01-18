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

#MULTICLASS CLASSIFICATION
# Classes: 1 is Jog, 2 is JogFall, 3 is Walk, 4 is WalkFall, 5 is stand, 6 is standFall,
# 7 is sit, 8 is sitFall, 9 is lie, 10 is lieFall, 11 is stairUp,
# 12 is stairUpFall, 13 is stairDown, 14 is stairDownFall

'''
Retrieve file name, gather features for SVM, runSVM
'''
def main():

        featureFile = input("Enter Training File: ")
        featureTestFile = input("Enter Test File: ")
        featureFile = open(featureFile, 'r')
        featureTestFile = open(featureTestFile, 'r')

        lines = featureFile.readlines()

        linesTest = featureTestFile.readlines()

        #GATHER FEATURES AND CLASSES AND INSERT INTO FILE
        X, CF, TestCF, TestX = gatherFeatures(lines, linesTest)

        #NORMALIZE DATA AND RUN THROUGH SVM OBJECT
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

        featuresLine = line.split(", ")

        #MAKES SURE ALL FEATURE LINES ARE THE SAME SIZE
        if(46 == len(featuresLine)):

            cfLine = line.split(", ")

            #APPEND ALL CLASSES THAT ARE FALLS
            if((int(cfLine[-1]) % 2) == 0):


                if (((int(cfLine[-1])) != 12) or ((int(cfLine[-1])) != 14)):

                    X.append(featuresLine[:-1])

                    CF.append(2)

            elif((int(cfLine[-1]) % 2) == 1):

                if (int(cfLine[-1]) == 7):

                    X.append(featuresLine[:-1])

                    CF.append(5)

                elif(((int(cfLine[-1])) == 9)):

                    X.append(featuresLine[:-1])

                    CF.append(5)

                elif(((int(cfLine[-1])) == 11) or ((int(cfLine[-1])) == 13)):

                    pass

                else:

                    X.append(featuresLine[:-1])

                    CF.append(int(cfLine[-1]))

    # TEST FILE
    for lineTest in linesTest:

        featuresLine = lineTest.split(", ")

        if(46 == len(featuresLine)):

            cfLine = lineTest.split(", ")

            # APPEND ALL CLASSES THAT ARE FALLS
            if ((int(cfLine[-1]) % 2) == 0):

                if (((int(cfLine[-1])) != 12) or ((int(cfLine[-1])) != 14)):

                    TestX.append(featuresLine[:-1])

                    TestCF.append(2)

            elif((int(cfLine[-1]) % 2) == 1):

                if (int(cfLine[-1]) == 7):

                    TestX.append(featuresLine[:-1])

                    TestCF.append(5)

                elif(((int(cfLine[-1])) == 9)):

                    TestX.append(featuresLine[:-1])

                    TestCF.append(5)

                elif(((int(cfLine[-1])) == 11) or ((int(cfLine[-1])) == 13)):

                    pass

                else:

                    TestX.append(featuresLine[:-1])

                    TestCF.append(int(cfLine[-1]))


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
    data = open("ResultsAccCombined.txt", "w")
    #data = open("dataMultiAcc.txt", "w")

    newClassifier = []

    knnandsvcClassifier = []

    randomandsvcClassifier = []

    treeandsvcClassifier = []

    allClassifier = []


    #ADD NEW PREDICTION HERE! AND COMBOS
    #LOOP THROUGH PREDICTIONS AND COMBINE RESULTS
    for i in range(len(predictedSVC)):

        #IF ANY PREDICTION IS FALL ADD FALL TO LIST!
        if((predictedSVC[i] == 2) or (predictedBayes[i] == 2)):

            newClassifier.append(2)

        else:

            newClassifier.append(predictedSVC[i])

        # IF ANY PREDICTION IS FALL ADD FALL TO LIST!
        if ((predictedSVC[i] == 2) or (predictedKNN[i] == 2)):

            knnandsvcClassifier.append(2)

        else:

            knnandsvcClassifier.append(predictedSVC[i])

        #IF ANY PREDICTION IS FALL ADD FALL TO LIST!
        if((predictedSVC[i] == 2) or (predictedTree[i] == 2)):

            treeandsvcClassifier.append(2)

        else:

            treeandsvcClassifier.append(predictedSVC[i])

        # IF ANY PREDICTION IS FALL ADD FALL TO LIST!
        if ((predictedSVC[i] == 2) or (predictedForest[i] == 2)):

            randomandsvcClassifier.append(2)

        else:

            randomandsvcClassifier.append(predictedSVC[i])

        if ((predictedSVC[i] == 2) or (predictedBayes[i] == 2) or (predictedForest[i] == 2) or (predictedTree[i] == 2) or (predictedKNN[i] == 2)):

            allClassifier.append(2)

        else:

            allClassifier.append(predictedSVC[i])

    # WRITE PREDICTED DATA
    data.write("PREDICTIONS FROM TEST DATA (SVC + NAIVE): \n" + str(newClassifier) + "\n\n")

    data.write(str(classification_report(listTestCF, newClassifier)) + '\n')

    accuracySVCandNaive = accuracy_score(cfTest, newClassifier)

    #WRITE ACCURACY
    data.write("\nACCURACY SVC + NAIVE: " + str(accuracySVCandNaive) + "\n\n")

    # WRITE PREDICTED DATA
    data.write("PREDICTIONS FROM TEST DATA (SVC + KNN): \n" + str(knnandsvcClassifier) + "\n\n")

    data.write(str(classification_report(listTestCF, knnandsvcClassifier)) + '\n')

    accuracySVCandKNN = accuracy_score(cfTest, knnandsvcClassifier)

    #WRITE ACCURACY
    data.write("\nACCURACY SVC + KNN: " + str(accuracySVCandKNN) + "\n\n")

    # WRITE PREDICTED DATA
    data.write("PREDICTIONS FROM TEST DATA (SVC + Tree): \n" + str(treeandsvcClassifier) + "\n\n")

    data.write(str(classification_report(listTestCF,treeandsvcClassifier)) + '\n')

    accuracySVCandTree = accuracy_score(cfTest, treeandsvcClassifier)

    #WRITE ACCURACY
    data.write("\nACCURACY SVC + Tree: " + str(accuracySVCandTree) + "\n\n")

    # WRITE PREDICTED DATA
    data.write("PREDICTIONS FROM TEST DATA (SVC + Forest): \n" + str(randomandsvcClassifier) + "\n\n")

    data.write(str(classification_report(listTestCF, randomandsvcClassifier)) + '\n')

    accuracySVCandRandom = accuracy_score(cfTest, randomandsvcClassifier)

    #WRITE ACCURACY
    data.write("\nACCURACY SVC + Forest: " + str(accuracySVCandRandom) + "\n\n")

    # WRITE PREDICTED DATA
    data.write("PREDICTIONS FROM TEST DATA (SVC + All): \n" + str(allClassifier) + "\n\n")

    data.write(str(classification_report(listTestCF, allClassifier)) + '\n')

    accuracySVCandAll = accuracy_score(cfTest, allClassifier)

    #WRITE ACCURACY
    data.write("\nACCURACY SVC + All: " + str(accuracySVCandAll) + "\n\n")

    #WRITE PREDICTED DATA
    data.write("PREDICTIONS FROM TEST DATA (SVC): \n" + str(predictedSVC) + "\n\n")
    data.write("PREDICTIONS FROM TEST DATA: (KNN)\n" + str(predictedKNN) + "\n\n")
    data.write("PREDICTIONS FROM TEST DATA: (Bayes)\n" + str(predictedBayes) + "\n\n")
    data.write("PREDICTIONS FROM TEST DATA: (Decision Tree)\n" + str(predictedTree) + "\n\n")
    data.write("PREDICTIONS FROM TEST DATA: (Random Forest)\n" + str(predictedForest) + "\n\n")

    #WRITE CONFUSION MATRIX
    data.write("CONFUSION MATRIX (SVC): \n")
    data.write(str(confusion_matrix(cfTest, predictedSVC)) + '\n\n\n\n')
    data.write(str(classification_report(listTestCF, predictedSVC)) + '\n')

    #WRITE CONFUSION MATRIX
    data.write("CONFUSION MATRIX: (KNN) \n")
    data.write(str(confusion_matrix(cfTest, predictedKNN)) + '\n\n\n')
    data.write(str(classification_report(listTestCF, predictedKNN)) + '\n')

    #WRITE CONFUSION MATRIX
    data.write("CONFUSION MATRIX: (BAYES) \n")
    data.write(str(confusion_matrix(cfTest, predictedBayes)) + '\n\n\n')
    data.write(str(classification_report(listTestCF, predictedBayes)) + '\n')

    #WRITE CONFUSION MATRIX
    data.write("CONFUSION MATRIX: (Decision Tree) \n")
    data.write(str(confusion_matrix(cfTest, predictedTree)) + '\n\n\n')
    data.write(str(classification_report(listTestCF, predictedTree)) + '\n')

    #WRITE CONFUSION MATRIX
    data.write("CONFUSION MATRIX: (Random Forest) \n")
    data.write(str(confusion_matrix(cfTest, predictedForest)) + '\n\n\n')
    data.write(str(classification_report(listTestCF, predictedForest)) + '\n')

    #ACCURACY
    accuracySVC = accuracy_score(cfTest, predictedSVC)
    accuracyKNN = accuracy_score(cfTest, predictedKNN)
    accuracyBayes = accuracy_score(cfTest, predictedBayes)
    accuracyTree = accuracy_score(cfTest, predictedTree)
    accuracyForest = accuracy_score(cfTest, predictedForest)
    accuracySVCandNaive = accuracy_score(cfTest, newClassifier)


    #WRITE ACCURACY
    data.write("\nACCURACY SVC: " + str(accuracySVC) + "\n\n")
    data.write("\nACCURACY KNN: " + str(accuracyKNN) + "\n\n")
    data.write("\nACCURACY BAYES: " + str(accuracyBayes) + "\n\n")
    data.write("\nACCURACY DECISION TREE: " + str(accuracyTree) + "\n\n")
    data.write("\nACCURACY RANDOM FOREST: " + str(accuracyForest) + "\n\n")


if __name__ == '__main__':
    main()











