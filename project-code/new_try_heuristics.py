# from heuristics import SentimentAnalyzer
from new_heuristics import SentimentAnalyzer

# function to print sentiments of the sentencee


def sentiment_scores(sentence):
    # Create a SentimentAnalyzer object.
    sid_obj = SentimentAnalyzer()
    # polarity_scores method of SentimentAnalyzer object gives a sentiment
    # dictionary which contains pos, neg, neu, and compound scores.
    sentiment_dict = sid_obj.polarity_scores(sentence)
    # print("\nOverall sentiment dictionary is : ", sentiment_dict, "\n")
    # print("Sentence Overall Rated As", end=" ")
    sentiment_score = 0.0
    OldMax = 4.0
    OldMin = -4.0
    NewMax = 10.0
    NewMin = 0.0
    OldRange = OldMax - OldMin
    NewRange = NewMax - NewMin

    # decide sentiment as positive, negative and neutral
    rating = sentiment_dict['compound']*10  # changing to scale of 10
    if sentiment_dict['compound'] >= 0.05:

        # new_rating = (((rating-1.0)*5.0)/4.0)+5.0
        new_rating = (((rating-OldMin)*NewRange)/OldRange)+NewMin

        if new_rating > 10.0:
            new_rating = 10.0
        sentiment_score = round(new_rating, 1)
    elif sentiment_dict['compound'] <= - 0.05:
        sentiment_dict['compound'] *= -1  # turn to positive
        new_rating = sentiment_dict['compound']*10  # change the scale to 10
        if new_rating > 5.00:
            new_rating = 10 - new_rating  # keep the negative rating below 5
        sentiment_score = round(new_rating, 1)
        if (sentiment_score < 1.0):
            sentiment_score = 1.0
    else:
        sentiment_dict['compound'] += 5.0  # make the neutral review at 5.
        new_rating = sentiment_dict['compound']
        sentiment_score = round(new_rating, 1)
    return sentiment_score
