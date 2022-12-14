import calculateWordsWithFreq
import main
import csv

finalPosFreqList = []
finalPosWordList = []
finalNegFreqList = []
finalNegWordList = []

lexDict = []

adjustedPosFreqList = []
adjustedNegFreqList = []

newClass = calculateWordsWithFreq.CalculateWordsWithFreq()
posFiles = main.processPositivefiles()
negFiles = main.processNegativefiles()


posResultList = newClass.wordsWithFreq(posFiles)
negResultList = newClass.negwordsWithFreq(negFiles)
newClass.checkDuplicate()

newPosresultList = newClass.customWordsAndFreqList
newNegresultList = newClass.negcustomWordsAndFreqList


for i in range(0, len(newPosresultList)):
    finalPosWordList.append(newPosresultList[i][0])
    finalPosFreqList.append(newPosresultList[i][1])

for i in range(0, len(newNegresultList)):
    finalNegWordList.append(newNegresultList[i][0])
    finalNegFreqList.append(newNegresultList[i][1])

# Converting old range to new range
# OldRange = (OldMax - OldMin) 500 - 0 = 500
# NewRange = (NewMax - NewMin)  4 - (-4) = 8
# NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin


NewMax = 4
NewMin = 0
OldRange = max(finalPosFreqList)
# print(OldRange)

NewRange = NewMax - NewMin

NewMaxNeg = -4
NewMinNeg = 0
OldRangeNeg = max(finalNegFreqList)
NewRangeNeg = NewMaxNeg - NewMinNeg

# Calculate the adjusted frequency list for the words


def calcValues():
    lengthpos = len(finalPosFreqList)
    lengthneg = len(finalNegFreqList)

    print("Total pos words: ", lengthpos)
    print("Total neg words: ", lengthneg)

    for f in range(lengthpos):
        adjustedPosFreqList.append(
            round(
                (((finalPosFreqList[f]*NewRange) / OldRange) + (NewMin)
                 ), 3))

    for f in range(lengthneg):
        adjustedNegFreqList.append(
            round(
                (((finalNegFreqList[f]*NewRangeNeg) / OldRangeNeg) + (NewMinNeg)
                 ), 3))

    adjustedPosFreqList.extend(adjustedNegFreqList)
    finalPosWordList.extend(finalNegWordList)


# Build lexicon out of the words and its corresponding adjusted value


def buildLexicon():
    for i in range(len(adjustedPosFreqList)):
        lexDict.append([finalPosWordList[i],
                       adjustedPosFreqList[i]])

    with open('project-code/LexiconDictionary.csv', 'w', newline='') as csvfile:
        my_writer = csv.writer(csvfile, delimiter=',')
        my_writer.writerows(lexDict)


calcValues()
buildLexicon()
