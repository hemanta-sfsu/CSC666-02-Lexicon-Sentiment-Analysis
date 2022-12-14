import os
import calculateWordsWithFreq
import cleaning
import new_try_heuristics

neg_directory = 'aclImdb/train/neg/'
pos_directory = 'aclImdb/train/pos/'
f1 = new_try_heuristics


# number of documents to read
n = 10000
pos_review_words = []
neg_review_words = []

# iterate thru filenames in a specified folder


def processPositivefiles():

    for filename in os.listdir(pos_directory)[:n]:
        fname = os.path.join(pos_directory, filename)
        # checking if it is a file and opening it
        if os.path.isfile(fname):
            # counting file
            with open(fname, encoding="utf8") as f:
                raw_words = f.read().split()
                sentence = ' '.join(raw_words)
                short_review = cleaning.text_clean(sentence)
                pos_review_words.append(short_review)

    positive_words = ' '.join(pos_review_words)

    return positive_words


def processNegativefiles():

    for filename in os.listdir(neg_directory)[:n]:
        fname = os.path.join(neg_directory, filename)
        # checking if it is a file and opening it
        if os.path.isfile(fname):
            # counting file
            with open(fname, encoding="utf8") as f:
                # print(filename)
                raw_words = f.read().split()
                sentence = ' '.join(raw_words)
                short_review = cleaning.text_clean(sentence)
                neg_review_words.append(short_review)

    negative_words = ' '.join(neg_review_words)
    return negative_words
