File that builds the lexicon: buildLexicon.py.
File that takes in the movie review that needs to be analyzed: sentimentAnalysis.py

*******************************************************
Note:
- There is no need to build the lexicon dictionary again. 
***************
Optional:
- If needed, just run the buildLexicon.py file. 
    - Changes can be made:
        - In calculateWordsWithFreq.py file, update the threshold value which is recorded with FILTER_NUMBER.
        - In main.py file, change the training dataset under neg_directory and pos_directory and number of files to use under variable "n". 
***************
- Current lexicon has 5,946 different word-score values. 
- Currently, the output has 1000 movie review - sentiment score values. 
- If any custom test is to be done, all the changes have to done in the sentimentAnalysis.py file.
- To update the file source:
    - Goto sentimentAnalysis.py file --> change the test_directory to the directory of the new file. 
    - Also update the name in line 17 and line 18 of the code (replace pos_directory with test_directory).
- If a custom review is to be tested:
    - update the "test_sentence" variable in the sentimentAnalysis.py file
    - replace  "sentence" in line 26 with "test_sentence".
    - For example: if the test sentence is "It was a good movie", update this string to the variable test_sentence and replace the variable "sentence" in line 26 with "test_sentence"

*******************************************************

In terminal: 

- To run the program: make run
- To clean the program cache: make clean
- To view the result: make view-result