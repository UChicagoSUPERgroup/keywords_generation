from nltk.stem import WordNetLemmatizer
import time
import pandas as pd


def singular(words):
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
    with open(infile, 'r') as f:
        data = f.readlines()

    data = [x.split(">")[-1].replace('\n', "").replace('&', 'and') for x in data if x != '\n']

    return data


search_terms = get_items()