File that builds the lexicon: buildLexicon.py.
File that takes in the movie review that needs to be analyzed: sentimentAnalysis.py

*******************************************************
Note:
- There is no need to build the lexicon dictionary again. 
- Current lexicon has 5,946 different word-score values. 
- Currently, the output has 1000 movie review - sentiment score values. 
- To update the file source, goto sentimentAnalysis.py file, change the test_directory to the directory of the new file. 
Also update this name in line 17 and line 18 of the code (replace pos_directory with test_directory).
- If a custom review is to be tested, update the "test_sentence" variable in the sentimentAnalysis.py file and 
replace  "sentence" in line 26 with "test_sentence"

*******************************************************

In terminal: 

To run the program: make run
To clean the program cache: make clean
To view the result: make view-result