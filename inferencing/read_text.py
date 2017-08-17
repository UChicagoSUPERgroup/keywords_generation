import requests
import json
from nltk.stem import WordNetLemmatizer
import urllib.request
import urllib.error
import pandas as pd
from nltk.stem import SnowballStemmer

import requests
from nltk import word_tokenize
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
import re
import string
import time


def preprocess_text_for_inference(text):
    tokens = word_tokenize(text)
    tokens = [
        t.lower()
        for t in tokens
        if t not in stopwords.words("english") and t not in string.punctuation
    ]
    # return tokens
    stemmer = SnowballStemmer('english')
    whole_ls = []
    for token in tokens:
        token = stemmer.stem(token)
        whole_ls.append(token)

    return whole_ls


USERAGENT = "'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'"


def get_text_from_url(url):
    headers = {
        'User-Agent': USERAGENT,
    }

    html = requests.get(url, headers=headers).text

    html = re.sub(r"<!--(.|\s|\n)*?-->", "", html)

    soup = BeautifulSoup(html, "lxml")

    body = soup.find("body")

    if body is not None:
        soup = body

    data = soup.findAll(text=True)

    def filter_tags(tag):
        if tag.parent.name in ['style', 'script', '[document]', 'head', 'title', 'footer']:
            return False
        classes = tag.findParents(class_=True)[:3]
        for c in classes:
            if "footer" in c:
                return False
        return True

    result = filter(filter_tags, data)

    return preprocess_text_for_inference(" ".join(list(result)))