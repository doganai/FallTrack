'''
Author: John Dogan
Counts the amount of samples in a feature file for non fall and fall.
'''

from collections import Counter

'''
Counts the amount of samples in a feature file
'''
def sampleCounter():

    fileName = input("Enter File Location: ")

    file = open(fileName, 'r')

    counter(file)

'''
Takes File and Counts All Valid Samples in Feature List
'''
def counter(file):

    lines = file.readlines()

    samples = []

    for line in lines:

        featuresLine = line.split()

        # MAKES SURE ALL FEATURE LINES ARE THE SAME SIZE
        if (46 == len(featuresLine)):

            samples.append(featuresLine[-1].replace("\n", " "))

    count = Counter(samples)

    print(count)

sampleCounter()
