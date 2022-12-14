import nltk


# helper functions for cleaning
def remove_punc(word):
    punc = '''-!()[]{};:"\,<>./?@#$%^&*_~'''
    no_punc_word = word.translate(str.maketrans('', '', punc))
    return no_punc_word


def remove_BR(lst):
    words = []
    for word in lst:
        if word.endswith('br'):
            word = word[:-2]
        words.append(word)

    return ' '.join(words)


def make_lower(word):
    return word.lower()


def remove_words(lst):
    extra_stops = ['aa', 'ab', 'br', 'us', 'mr', 'saw', 'until', 'no', 'when', 'with',
                   'like', 'just', 'even', 'it\'s', 'i\'m',
                   'who', 'i\'ve', 'what', 'he', 'see', 'up', 'get', 'been',
                   'because', 'into', 'time', 'watch', 'â–', 'called', '2',
                   '10', 'said', 'their', 'then', 'can', 'two', 'go', 'also', 'seen', 'him',
                   'through', 'it', 'doesn\'t', 'you\'re', 'that\'s', 'there\'s',
                   'come', 'said', 'all.', 'screen', 'person', 'i\'ll', 'is,'
                   '5', 'sandra', 'them.', '3', '.', 'he\'s', 'man', 'they\'re',
                   '\\\x96', '--', 'i\'d', 'is,', 'oh', 'one', 'much', 'movies',
                   'say', '4', '1', 'five', 'what\'s', '15', 'ed', '...', '"',
                   'movie', 'film', '', '-', 'people', 'could', 'make', 'films', 'reviews', 'is', 'are']

    stop_words = nltk.corpus.stopwords.words("english")
    stop_words = set(stop_words)
    stop_words.update(extra_stops)

    words = [word for word in lst if word not in stop_words]

    return ' '.join(words)


def text_clean(message):
    message = remove_punc(message)   # remove punctiation except - and \'
    message = remove_words(message.split())
    message = remove_BR(message.split())
    # message = remove_numbers(message.split())
    message = nltk.tag.pos_tag(message.split(), tagset='universal')
    message = [word for word, tag in message if (
        tag == 'ADJ' or tag == 'ADV' or tag == 'VERB')]
    message = ' '.join(message)
    message = message.lower()

    return message
