from nltk.corpus import wordnet as wn
from nltk.stem import SnowballStemmer
from nltk import word_tokenize, pos_tag, corpus
import nltk


def synonyms(word):
    stemmer = SnowballStemmer("english")
    syns = wn.synsets(word)
    res = []
    for x in syns:
        print(x)
        res += x.lemma_names()

    res = [stemmer.stem(x) for x in res]
    res = list(set(res))

    return res

print(synonyms("ordered"))