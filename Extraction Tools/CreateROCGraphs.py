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
from sklearn.metrics import roc_curve
from sklearn.metrics import auc
import matplotlib.pyplot as plt
#USE THIS PACKAGE TO EXPORT FOR JAVA
from sklearn_porter import Porter

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

                    CF.append(1)

                elif(((int(cfLine[-1])) == 9)):

                    X.append(featuresLine[:-1])

                    CF.append(1)

                elif(((int(cfLine[-1])) == 11) or ((int(cfLine[-1])) == 13)):

                    pass

                else:

                    X.append(featuresLine[:-1])

                    CF.append(1)

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

                    TestCF.append(1)

                elif(((int(cfLine[-1])) == 9)):

                    TestX.append(featuresLine[:-1])

                    TestCF.append(1)

                elif(((int(cfLine[-1])) == 11) or ((int(cfLine[-1])) == 13)):

                    pass

                else:

                    TestX.append(featuresLine[:-1])

                    TestCF.append(1)


    return X, CF, TestCF, TestX;

'''
ListX: 
listTestX:
listTestCF:
CF:
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
    rbf_svc = SVC(kernel='rbf', gamma=0.00001, C=1000,probability=True).fit(X, cf)

    #K NEIGHBOR GATHER DATA
    knn = KNeighborsClassifier(n_neighbors=1).fit(X, cf)

    #NAIVE BAYES GATHER DATA
    gnb = GaussianNB().fit(X, cf)

    #DECISION TREE
    dTree = tree.DecisionTreeClassifier().fit(X, cf)

    #RANDOM FOREST
    rForest = RandomForestClassifier(n_estimators=15, max_depth=None).fit(X, cf)

    #PREDICT PROBABILITY SCORE = 2D ARRAY FOR EACH PREDICTION
    predictedprobSVC = rbf_svc.predict_proba(TestX)
    predictedprobKNN = knn.predict_proba(TestX)
    predictedprobBayes = gnb.predict_proba(TestX);
    predictedprobTree = dTree.predict_proba(TestX);
    predictedprobForest = rForest.predict_proba(TestX)

    predictedSVC= rbf_svc.predict(TestX);
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
    data = open("ROCResults.txt", "w")
    #data = open("dataMultiAcc.txt", "w")

    #SVC AND BAYES
    #Fused Probability
    svcAndBayesClassifierProb = []
    knnandsvcClassifierProb = []
    randomandsvcClassifierProb = []
    treeandsvcClassifierProb = []
    allClassifierProb = []

    #Get Results
    newClassifier = []
    knnandsvcClassifier = []
    randomandsvcClassifier = []
    treeandsvcClassifier = []
    allClassifier = []


    countList = []

    #ADD NEW PREDICTION HERE! AND COMBOS
    #LOOP THROUGH PREDICTIONS AND COMBINE RESULTS
    #GATHER PROBABILITY SCORE
    for i in range(len(predictedSVC)):

            countList.append(i+1)

            #CREATE FUSED PROBABILITY SCORE
            svcAndBayesClassifierProb.append((float(predictedprobSVC[i][1])+float(predictedprobBayes[i][1]))/2)
            knnandsvcClassifierProb.append((float(predictedprobSVC[i][1])+float(predictedprobKNN[i][1]))/2)
            treeandsvcClassifierProb.append((float(predictedprobSVC[i][1])+float(predictedprobTree[i][1]))/2)
            randomandsvcClassifierProb.append((float(predictedprobSVC[i][1])+float(predictedprobForest[i][1]))/2)
            allClassifierProb.append((float(predictedprobSVC[i][1])+float(predictedprobForest[i][1])+float(predictedprobTree[i][1])+float(predictedprobBayes[i][1])+float(predictedprobKNN[i][1]))/5)

            # IF ANY PREDICTION IS FALL ADD FALL TO LIST!
            if ((predictedSVC[i] == 2) or (predictedBayes[i] == 2)):

                newClassifier.append(2)

            else:

                newClassifier.append(predictedSVC[i])

            # IF ANY PREDICTION IS FALL ADD FALL TO LIST!
            if ((predictedSVC[i] == 2) or (predictedKNN[i] == 2)):

                knnandsvcClassifier.append(2)

            else:

                knnandsvcClassifier.append(predictedSVC[i])

            # IF ANY PREDICTION IS FALL ADD FALL TO LIST!
            if ((predictedSVC[i] == 2) or (predictedTree[i] == 2)):

                treeandsvcClassifier.append(2)

            else:

                treeandsvcClassifier.append(predictedSVC[i])

            # IF ANY PREDICTION IS FALL ADD FALL TO LIST!
            if ((predictedSVC[i] == 2) or (predictedForest[i] == 2)):

                randomandsvcClassifier.append(2)

            else:

                randomandsvcClassifier.append(predictedSVC[i])

            if ((predictedSVC[i] == 2) or (predictedBayes[i] == 2) or (predictedForest[i] == 2) or (
                    predictedTree[i] == 2) or (predictedKNN[i] == 2)):

                allClassifier.append(2)

            else:

                allClassifier.append(predictedSVC[i])


    #GET ROC DATA
    fpr1, tpr1, thresholds = roc_curve(cfTest,svcAndBayesClassifierProb,pos_label=2)
    roc_auc1 = auc(fpr1, tpr1)
    fpr2, tpr2, thresholds = roc_curve(cfTest,treeandsvcClassifierProb,pos_label=2)
    roc_auc2 = auc(fpr2, tpr2)
    fpr3, tpr3, thresholds = roc_curve(cfTest,randomandsvcClassifierProb,pos_label=2)
    roc_auc3 = auc(fpr3, tpr3)
    fpr4, tpr4, thresholds = roc_curve(cfTest,knnandsvcClassifierProb,pos_label=2)
    roc_auc4 = auc(fpr4, tpr4)
    fpr5, tpr5, thresholds = roc_curve(cfTest, predictedprobSVC[:,1], pos_label=2)
    roc_auc5 = auc(fpr5, tpr5)
    fpr6, tpr6, thresholds = roc_curve(cfTest, predictedprobKNN[:,1], pos_label=2)
    roc_auc6 = auc(fpr6, tpr6)
    fpr7, tpr7, thresholds = roc_curve(cfTest, predictedprobForest[:,1], pos_label=2)
    roc_auc7 = auc(fpr7, tpr7)
    fpr8, tpr8, thresholds = roc_curve(cfTest, predictedprobTree[:,1], pos_label=2)
    roc_auc8 = auc(fpr8, tpr8)
    fpr9, tpr9, thresholds = roc_curve(cfTest, predictedprobBayes[:, 1], pos_label=2)
    roc_auc9 = auc(fpr9, tpr9)
    fpr10, tpr10, thresholds = roc_curve(cfTest, allClassifierProb, pos_label=2)
    roc_auc10 = auc(fpr10, tpr10)

    #GRAPH DATA
    plt.figure()
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.plot([0, 1], [0, 1], color='navy', linestyle='--')
    #plt.title('Gyroscope Classifiers ROC')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.plot(fpr1,tpr1,color='orange', lw=2, label='SVM + Naive Bayes ROC (area = %0.2f)' % roc_auc1)
    plt.plot(fpr2, tpr2, color='green', lw=2, label='SVM + Decision Tree ROC (area = %0.2f)' % roc_auc2)
    plt.plot(fpr3, tpr3, color='purple', lw=2, label='SVM + Random Forest ROC (area = %0.2f)' % roc_auc3)
    plt.plot(fpr4, tpr4, color='yellow', lw=2, label='SVM + KNN ROC curve (area = %0.2f)' % roc_auc4)
    plt.plot(fpr5, tpr5, color='blue', lw=2, label='SVM ROC area = %0.2f)' % roc_auc5)
    plt.plot(fpr6, tpr6, color='gray', lw=2, label='KNN ROC (area = %0.2f)' % roc_auc6)
    plt.plot(fpr7, tpr7, color='black', lw=2, label='Random Forest ROC  (area = %0.2f)' % roc_auc7)
    plt.plot(fpr8, tpr8, color='cyan', lw=2, label='Decision Tree ROC (area = %0.2f)' % roc_auc8)
    plt.plot(fpr9, tpr9, color='orange', lw=2, label='Naive Bayes ROC (area = %0.2f)' % roc_auc9)
    plt.plot(fpr10, tpr10, color='red', lw=2, label='All Classifiers ROC (area = %0.2f)' % roc_auc10)
    plt.legend(loc="lower right")
    plt.show()

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


    #WRITE ACCURACY
    data.write("\nACCURACY SVC: " + str(accuracySVC) + "\n\n")
    data.write("\nACCURACY KNN: " + str(accuracyKNN) + "\n\n")
    data.write("\nACCURACY BAYES: " + str(accuracyBayes) + "\n\n")
    data.write("\nACCURACY DECISION TREE: " + str(accuracyTree) + "\n\n")
    data.write("\nACCURACY RANDOM FOREST: " + str(accuracyForest) + "\n\n")

    # export:
    porter = Porter(rbf_svc, language='java')
    output = porter.export(embed_data=True)
    print(output)


if __name__ == '__main__':
    main()











