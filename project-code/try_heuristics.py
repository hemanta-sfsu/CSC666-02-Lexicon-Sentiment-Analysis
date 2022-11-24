from heuristics import SentimentAnalyzer
import csv


# function to print sentiments of the sentencee
def sentiment_scores(sentence):
    # Create a SentimentAnalyzer object.
    sid_obj = SentimentAnalyzer()
    # polarity_scores method of SentimentAnalyzer object gives a sentiment
    # dictionary which contains pos, neg, neu, and compound scores.
    sentiment_dict = sid_obj.polarity_scores(sentence)
    print("\nOverall sentiment dictionary is : ", sentiment_dict, "\n")
    print("Sentence Overall Rated As", end=" ")
    sentiment_score = 0.0

    # decide sentiment as positive, negative and neutral
    rating = sentiment_dict['compound']*10  # changing to scale of 10
    if sentiment_dict['compound'] >= 0.05:
       # Converting old range to new range
       # OldRange = (OldMax - OldMin)
       # NewRange = (NewMax - NewMin)
       # NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin

        new_rating = (((rating-1.0)*5.0)/4.0)+5.0
        if new_rating > 10.0:
            new_rating = 10.0
        sentiment_score = round(new_rating, 1)
        print("Positive. Sentiment Score: ", sentiment_score, "/10.0")
    elif sentiment_dict['compound'] <= - 0.05:
        sentiment_dict['compound'] *= -1  # turn to positive
        new_rating = sentiment_dict['compound']*10  # change the scale to 10
        if new_rating > 5.00:
            new_rating = 10 - new_rating  # keep the negative rating below 5
        sentiment_score = round(new_rating, 1)
        print("Negative. Sentiment Score: ", sentiment_score, "/10.0")
    else:
        sentiment_dict['compound'] += 5.0  # make the neutral review at 5.
        new_rating = sentiment_dict['compound']
        sentiment_score = round(new_rating, 1)
        print("Neutral. Sentiment Score: ", sentiment_score, "/10.0")

    return sentiment_score


# Main code
if __name__ == "__main__":

    # 1 '''Using the given set of files as input'''
    # path = "aclImdb/test/pos/0_10.txt"

    # with open(path) as f:
    #     lines = f.readlines()

    # print("Text Selected for VADER Sentimental Analysis :\n")
    # sentence1 = lines[0]
    # print("\n", sentence1)
    ##

    # 2 '''Using custom input'''
    analyzer = SentimentAnalyzer()
    sentences = ["It was a good movie",
                 "It was a absolutely good movie",
                 "It was almost a good movie",
                 "It was a bad movie",
                 "It was a very bad movie",
                 "It was a BAD movie", ]

    for sentence in sentences:
        print("=====================================")
        print("\n", sentence)
        sentiment_scores(sentence)
        print("=====================================")

    ###

    ## '''exporting as csv'''
    # 2D list of variables (tabular data with rows and columns)
    reviews = [
        ['Reviews\t\t\t\t\t\t\t\t||',
            'Sentiment (0=Worst, 5=Neutral 10=Best)'],
        [sentences[0], '\t\t\t\t\t', sentiment_scores(sentences[0])],
        (sentences[1], '\t\t', sentiment_scores(sentences[1])),
        (sentences[2], '\t\t\t', sentiment_scores(sentences[2])),
        (sentences[3], '\t\t\t\t\t', sentiment_scores(sentences[3])),
        (sentences[4], '\t\t\t\t', sentiment_scores(sentences[4])),
        (sentences[5], '\t\t\t\t\t', sentiment_scores(sentences[5]))
    ]

    for i in sentiment_scores(sentences):
        

    reviews = [
        ['Negative (0-4.9)\t\t\t\t\t\t\t\t||',
            'Neutral (5.0-5.9)\t\t\t\t\t\t\t\t||', 'Positive (6.0-10.0)'],
        [sentences[0], '\t\t\t\t\t', sentiment_scores(sentences[0])],
        (sentences[1], '\t\t', sentiment_scores(sentences[1])),
        (sentences[2], '\t\t\t', sentiment_scores(sentences[2])),
        (sentences[3], '\t\t\t\t\t', sentiment_scores(sentences[3])),
        (sentences[4], '\t\t\t\t', sentiment_scores(sentences[4])),
        (sentences[5], '\t\t\t\t\t', sentiment_scores(sentences[5]))
    ]

    with open('Sentiment_scores.csv', 'w', newline='') as csvfile:
        my_writer = csv.writer(csvfile, delimiter=' ')
        my_writer.writerows(reviews)
    ###


# 1 function calling for input file
# sentiment_scores(sentence1)
