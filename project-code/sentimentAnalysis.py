import os
import cleaning
import csv
import new_try_heuristics

neg_directory = 'aclImdb/train/neg/'
pos_directory = 'aclImdb/train/pos/'
test_directory = 'aclImdb/train/unsup/'
f1 = new_try_heuristics
n = 1000
reviews = [['Reviews\t\t\t\t\t\t\t||',
           'Sentiment (0=Worst, 5=Neutral 10=Best)']]


def exportSentiment():
    for filename in os.listdir(pos_directory)[:n]:
        fname = os.path.join(pos_directory, filename)
        # checking if it is a file and opening it
        if os.path.isfile(fname):
            # counting file
            with open(fname, encoding="utf8") as f:
                raw_words = f.read().split()
                sentence = ' '.join(raw_words)
                reviews.append(
                    [sentence[:70],  f1.sentiment_scores(sentence)])

                with open('./project-code/Sentiment_Scores.csv', 'w', newline='') as csvfile:
                    my_writer = csv.writer(csvfile, delimiter='\t')
                    my_writer.writerows(reviews)


print("\nRun Successful! View the result by running 'make view-result' \n")
exportSentiment()
