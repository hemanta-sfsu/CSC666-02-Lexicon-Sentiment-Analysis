# Full version of this code can be found
# @ https://github.com/cjhutto/vaderSentiment/blob/master/vaderSentiment/vaderSentiment.py

import os
import math
import string
import codecs
from inspect import getsourcefile
from io import open


'''
Heuristics: 
    Capitalization: good vs GOOD
    Degree modifier: 
        Booster: "good movie" vs "absolutely good movie"
        Damper words: "good movie" vs "almost good movie"
'''
# Constants:
# B_WO = booster words
# D_WO = damper words
# C_WO = capital words

# Values from vader
# (empirically derived mean sentiment intensity rating increase for booster words)
B_WO = 0.293
D_WO = -0.293
C_WO = 0.733
N_SCALAR = -0.74


NEGATE = \
    ["aint", "arent", "cannot", "cant", "couldnt", "darent", "didnt", "doesnt",
     "ain't", "aren't", "can't", "couldn't", "daren't", "didn't", "doesn't",
     "dont", "hadnt", "hasnt", "havent", "isnt", "mightnt", "mustnt", "neither",
     "don't", "hadn't", "hasn't", "haven't", "isn't", "mightn't", "mustn't",
     "neednt", "needn't", "never", "none", "nope", "nor", "not", "nothing", "nowhere",
     "oughtnt", "shant", "shouldnt", "uhuh", "wasnt", "werent",
     "oughtn't", "shan't", "shouldn't", "uh-uh", "wasn't", "weren't",
     "without", "wont", "wouldnt", "won't", "wouldn't", "rarely", "seldom", "despite"]


BOOSTER_DICT = \
    {"absolutely": B_WO, "amazingly": B_WO, "awfully": B_WO,
     "completely": B_WO, "considerable": B_WO, "considerably": B_WO,
     "decidedly": B_WO, "deeply": B_WO, "effing": B_WO, "enormous": B_WO, "enormously": B_WO,
     "entirely": B_WO, "especially": B_WO, "exceptional": B_WO, "exceptionally": B_WO,
     "extreme": B_WO, "extremely": B_WO,
     "fabulously": B_WO, "flipping": B_WO, "flippin": B_WO, "frackin": B_WO, "fracking": B_WO,
     "fricking": B_WO, "frickin": B_WO, "frigging": B_WO, "friggin": B_WO, "fully": B_WO,
     "fuckin": B_WO, "fucking": B_WO, "fuggin": B_WO, "fugging": B_WO,
     "greatly": B_WO, "hella": B_WO, "highly": B_WO, "hugely": B_WO,
     "incredible": B_WO, "incredibly": B_WO, "intensely": B_WO,
     "major": B_WO, "majorly": B_WO, "more": B_WO, "most": B_WO, "particularly": B_WO,
     "purely": B_WO, "quite": B_WO, "really": B_WO, "remarkably": B_WO,
     "so": B_WO, "substantially": B_WO,
     "thoroughly": B_WO, "total": B_WO, "totally": B_WO, "tremendous": B_WO, "tremendously": B_WO,
     "uber": B_WO, "unbelievably": B_WO, "unusually": B_WO, "utter": B_WO, "utterly": B_WO,
     "very": B_WO,

     "almost": D_WO, "barely": D_WO, "hardly": D_WO, "just enough": D_WO,
     "kind of": D_WO, "kinda": D_WO, "kindof": D_WO, "kind-of": D_WO,
     "less": D_WO, "little": D_WO, "marginal": D_WO, "marginally": D_WO,
     "occasional": D_WO, "occasionally": D_WO, "partly": D_WO,
     "scarce": D_WO, "scarcely": D_WO, "slight": D_WO, "slightly": D_WO, "somewhat": D_WO,
     "sort of": D_WO, "sorta": D_WO, "sortof": D_WO, "sort-of": D_WO}


def negated(input_words, include_nt=True):
    """
    Determine if input contains negation words
    """
    input_words = [str(w).lower() for w in input_words]
    neg_words = []
    neg_words.extend(NEGATE)
    for word in neg_words:
        if word in input_words:
            return True
    if include_nt:
        for word in input_words:
            if "n't" in word:
                return True
    '''if "least" in input_words:
        i = input_words.index("least")
        if i > 0 and input_words[i - 1] != "at":
            return True'''
    return False
# normalizing function from vader sentiment


def normalize(score, alpha=15):
    """
    Normalize the score to be between -1 and 1 using an alpha that
    approximates the max expected value
    """
    norm_score = score / math.sqrt((score * score) + alpha)
    if norm_score < -1.0:
        return -1.0
    elif norm_score > 1.0:
        return 1.0
    else:
        return norm_score


def handle_capital(words):
    """
    Check whether just some words in the input are ALL CAPS
    :param list words: The words to inspect
    :returns: `True` if some but not all items in `words` are ALL CAPS
    """
    is_different = False
    allcap_words = 0
    for word in words:
        if word.isupper():
            allcap_words += 1
    cap_differential = len(words) - allcap_words
    if 0 < cap_differential < len(words):
        is_different = True
    return is_different


def scalar_inc_dec(word, valence, is_cap_diff):
    """
    Check if the preceding words increase, decrease, or negate/nullify the
    valence
    """
    scalar = 0.0
    word_lower = word.lower()
    if word_lower in BOOSTER_DICT:
        scalar = BOOSTER_DICT[word_lower]
        if valence < 0:
            scalar *= -1
        # check if booster/dampener word is in ALLCAPS (while others aren't)
        if word.isupper() and is_cap_diff:
            if valence > 0:
                scalar += C_WO
            else:
                scalar -= C_WO
    return scalar

# basically bag of words


class SentiText(object):
    """
    Identify sentiment-relevant string-level properties of input text.
    """

    def __init__(self, text):
        # if not isinstance(text, str):
        #     text = str(text).encode('utf-8')
        self.text = text
        self.words_ = self._words_()
        # doesn't separate words from
        # adjacent punctuation (keeps emoticons & contractions)
        self.is_cap_diff = handle_capital(self.words_)

    @staticmethod
    def _strip_punc_if_word(token):
        """
        Removes all trailing and leading punctuation
        If the resulting string has two or fewer characters,
        then it was likely an emoticon, so return original string
        (ie ":)" stripped would be "", so just return ":)"
        """
        stripped = token.strip(string.punctuation)
        if len(stripped) <= 2:
            return token
        return stripped

    def _words_(self):
        """
        Removes leading and trailing puncutation
        Leaves contractions and most emoticons
            Does not preserve punc-plus-letter emoticons (e.g. :D)
        """
        words = self.text.split()
        stripped = list(map(self._strip_punc_if_word, words))
        return stripped


class SentimentAnalyzer(object):
    def __init__(self, lexicon_file="LexiconDictionary.csv"):
        _this_module_file_path_ = os.path.abspath(getsourcefile(lambda: 0))
        lexicon_full_filepath = os.path.join(
            os.path.dirname(_this_module_file_path_), lexicon_file)
        with codecs.open(lexicon_full_filepath, encoding='utf-8') as f:
            self.lexicon_full_filepath = f.read()
        self.lexicon = self.make_lex_dict()

    def make_lex_dict(self):
        """
        Convert lexicon file to a dictionary
        """
        lex_dict = {}
        for line in self.lexicon_full_filepath.rstrip('\n').split('\n'):
            if not line:
                continue
            (word, measure) = line.strip().split(',')[0:2]
            lex_dict[word] = float(measure)
        return lex_dict

    def polarity_scores(self, text):
        """
        Return a float for sentiment strength based on the input text.
        Positive values are positive valence, negative value are negative
        valence.
        """

        sentitext = SentiText(text)

        sentiments = []
        words_ = sentitext.words_
        for i, item in enumerate(words_):
            valence = 0
            # check for vader_lexicon words that may be used as modifiers
            if item.lower() in BOOSTER_DICT:
                sentiments.append(valence)
                continue
            sentiments = self.sentiment_valence(
                valence, sentitext, item, i, sentiments)

        sentiments = self._but_check(words_, sentiments)

        valence_dict = self.score_valence(sentiments, text)

        return valence_dict

    def sentiment_valence(self, valence, sentitext, item, i, sentiments):
        is_cap_diff = sentitext.is_cap_diff
        words_ = sentitext.words_
        item_lowercase = item.lower()
        if item_lowercase in self.lexicon:
            # get the sentiment valence
            valence = self.lexicon[item_lowercase]

            # check for "no" as negation for an adjacent lexicon item vs "no" as its own stand-alone lexicon item
            if item_lowercase == "no" and i != len(words_)-1 and words_[i + 1].lower() in self.lexicon:
                # don't use valence of "no" as a lexicon item. Instead set it's valence to 0.0 and negate the next item
                valence = 0.0
            if (i > 0 and words_[i - 1].lower() == "no") \
               or (i > 1 and words_[i - 2].lower() == "no") \
               or (i > 2 and words_[i - 3].lower() == "no" and words_[i - 1].lower() in ["or", "nor"]):
                valence = self.lexicon[item_lowercase] * N_SCALAR

            # check if sentiment laden word is in ALL CAPS (while others aren't)
            if item.isupper() and is_cap_diff:
                if valence > 0:
                    valence += C_WO
                else:
                    valence -= C_WO

            for start_i in range(0, 3):
                # dampen the scalar modifier of preceding words and emoticons
                # (excluding the ones that immediately preceed the item) based
                # on their distance from the current item.
                if i > start_i and words_[i - (start_i + 1)].lower() not in self.lexicon:
                    s = scalar_inc_dec(
                        words_[i - (start_i + 1)], valence, is_cap_diff)
                    if start_i == 1 and s != 0:
                        s = s * 0.95
                    if start_i == 2 and s != 0:
                        s = s * 0.9
                    valence = valence + s

        sentiments.append(valence)
        return sentiments

    @staticmethod
    def _but_check(words_and_emoticons, sentiments):
        # check for modification in sentiment due to contrastive conjunction 'but'
        words_and_emoticons_lower = [str(w).lower()
                                     for w in words_and_emoticons]
        if 'but' in words_and_emoticons_lower:
            bi = words_and_emoticons_lower.index('but')
            for sentiment in sentiments:
                si = sentiments.index(sentiment)
                if si < bi:
                    sentiments.pop(si)
                    sentiments.insert(si, sentiment * 0.5)
                elif si > bi:
                    sentiments.pop(si)
                    sentiments.insert(si, sentiment * 1.5)
        return sentiments

    @staticmethod
    def _negation_check(valence, words_and_emoticons, start_i, i):
        words_and_emoticons_lower = [str(w).lower()
                                     for w in words_and_emoticons]
        if start_i == 0:
            # 1 word preceding lexicon word (w/o stopwords)
            if negated([words_and_emoticons_lower[i - (start_i + 1)]]):
                valence = valence * N_SCALAR
        if start_i == 1:
            if words_and_emoticons_lower[i - 2] == "never" and \
                    (words_and_emoticons_lower[i - 1] == "so" or
                     words_and_emoticons_lower[i - 1] == "this"):
                valence = valence * 1.25
            elif words_and_emoticons_lower[i - 2] == "without" and \
                    words_and_emoticons_lower[i - 1] == "doubt":
                valence = valence
            # 2 words preceding the lexicon word position
            elif negated([words_and_emoticons_lower[i - (start_i + 1)]]):
                valence = valence * N_SCALAR
        if start_i == 2:
            if words_and_emoticons_lower[i - 3] == "never" and \
                    (words_and_emoticons_lower[i - 2] == "so" or words_and_emoticons_lower[i - 2] == "this") or \
                    (words_and_emoticons_lower[i - 1] == "so" or words_and_emoticons_lower[i - 1] == "this"):
                valence = valence * 1.25
            elif words_and_emoticons_lower[i - 3] == "without" and \
                    (words_and_emoticons_lower[i - 2] == "doubt" or words_and_emoticons_lower[i - 1] == "doubt"):
                valence = valence
            # 3 words preceding the lexicon word position
            elif negated([words_and_emoticons_lower[i - (start_i + 1)]]):
                valence = valence * N_SCALAR
        return valence

    @staticmethod
    def _sift_sentiment_scores(sentiments):
        # want separate positive versus negative sentiment scores
        pos_sum = 0.0
        neg_sum = 0.0
        neu_count = 0
        for sentiment_score in sentiments:
            if sentiment_score > 0:
                # compensates for neutral words that are counted as 1
                pos_sum += (float(sentiment_score) + 1)
            if sentiment_score < 0:
                # when used with math.fabs(), compensates for neutrals
                neg_sum += (float(sentiment_score) - 1)
            if sentiment_score == 0:
                neu_count += 1
        return pos_sum, neg_sum, neu_count

    def score_valence(self, sentiments, text):
        if sentiments:
            sum_s = float(sum(sentiments))

            compound = normalize(sum_s)

            # discriminate between positive, negative and neutral sentiment scores
            pos_sum, neg_sum, neu_count = self._sift_sentiment_scores(
                sentiments)

            total = pos_sum + math.fabs(neg_sum) + neu_count
            pos = math.fabs(pos_sum / total)
            neg = math.fabs(neg_sum / total)
            neu = math.fabs(neu_count / total)

        else:
            compound = 0.0
            pos = 0.0
            neg = 0.0
            neu = 0.0

        sentiment_dict = \
            {"neg": round(neg, 3),
             "neu": round(neu, 3),
             "pos": round(pos, 3),
             "compound": round(compound, 4)}

        return sentiment_dict
