from nltk.stem import WordNetLemmatizer


def singular(words):
    '''Get the singular version of a list of words with NLTK lemmatizer'''
    wnl = WordNetLemmatizer()
    words = words.split(" ")
    ls = []
    for word in words:
        if word.isupper():
            ls.append(word)
        else:
            ls.append(word.lower())
    words = [wnl.lemmatize(word) for word in ls]
    words = " ".join(words)

    return words


def get_items(infile="interest.txt"):
    '''Get the wikipedia searching term from the Google Ads Interests Categories'''
    with open(infile, 'r') as f:
        data = f.readlines()

    '''Change "&" to "and, because wikipedia API doesn't read &"'''
    data = [x.split(">")[-1].replace('\n', "").replace('&', 'and') for x in data if x != '\n']

    return data


'''Get the terms of each category, and ready to export'''
search_terms = get_items()
