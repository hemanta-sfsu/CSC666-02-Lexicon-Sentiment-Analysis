class CalculateWordsWithFreq:
    # For positive Calculation
    wordsList = []
    freqList = []
    wordsFreqList = dict()
    allWordsAndFreqList = []
    customWordsAndFreqList = []

    # For negative Calculation
    negwordsList = []
    negfreqList = []
    negwordsFreqList = dict()
    negallWordsAndFreqList = []
    negcustomWordsAndFreqList = []

    # Filter the frequency threshold for building lexicon
    FILTER_NUMBER = 10

    finalPosWordList = []
    finalPosFreqList = []

    def wordsWithFreq(self, str):

        # break the string into list of words
        str = str.split()

        # loop till string values present in list str
        for i in str:
            if i not in self.wordsList:
                self.wordsList.append(i)

        for i in range(0, len(self.wordsList)):

            # count the frequency of each word(present
            self.freqList.append(str.count(self.wordsList[i]))
            self.wordsFreqList[self.wordsList[i]] = self.freqList[i]

        for w in sorted(self.wordsFreqList, key=self.wordsFreqList.get, reverse=True):
            self.allWordsAndFreqList.append([w, self.wordsFreqList[w]])
            if (self.wordsFreqList[w] > self.FILTER_NUMBER):
                self.customWordsAndFreqList.append(
                    [w, self.wordsFreqList[w]])
        return self.allWordsAndFreqList, self.customWordsAndFreqList

    def negwordsWithFreq(self, str):

        # break the string into list of words
        str = str.split()

        # loop till string values present in list str
        for i in str:
            if i not in self.negwordsList:
                self.negwordsList.append(i)

        for i in range(0, len(self.negwordsList)):

            # count the frequency of each word(present
            self.negfreqList.append(str.count(self.negwordsList[i]))
            self.negwordsFreqList[self.negwordsList[i]] = self.negfreqList[i]

        for w in sorted(self.negwordsFreqList, key=self.negwordsFreqList.get, reverse=True):
            self.negallWordsAndFreqList.append([w, self.negwordsFreqList[w]])
            if (self.negwordsFreqList[w] > self.FILTER_NUMBER):
                self.negcustomWordsAndFreqList.append(
                    [w, self.negwordsFreqList[w]])

        return self.negallWordsAndFreqList, self.negcustomWordsAndFreqList

    def checkDuplicate(self):

        dupList = []
        if (self.customWordsAndFreqList):
            for pos in self.customWordsAndFreqList:
                for neg in self.negcustomWordsAndFreqList:
                    if (pos[0].__eq__(neg[0])):
                        dupList.append(neg)

                        if ((pos[1] > 3.0) or (neg[1] > -1.0)):
                            newFreq = (pos[1]-neg[1])
                            pos[1] = newFreq

                        elif ((pos[1] <= 1.0) or (neg[1] <= -3.0)):
                            newFreq = (-1)*((pos[1]-neg[1])/1.1)
                            pos[1] = newFreq

        for dup in dupList:
            for words in self.negcustomWordsAndFreqList:
                if (dup[0].__eq__(words[0])):
                    self.negcustomWordsAndFreqList.remove(words)
