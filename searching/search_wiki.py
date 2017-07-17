import re
from timeit import timeit
import requests
import math
import pandas as pd
from nltk.corpus import wordnet as wn
import sys
from search_term import search_terms

sys.path.append("/Users/sixiongshan/Desktop/inferencing_keywords/searching/exclusion")
from exclusion.search_regions import is_region, is_spec


def to_exclude(cat, title, snippet, region=True):
    all_letter = re.findall(r"[a-zA-Z ]+", title)
    if len(all_letter) > 1:
        return True

    is_ls = re.search("([Ll]ist)", title)
    if is_ls is not None:
        return True

    text = " ".join([title, snippet])
    if not region:
        return is_spec(text)

    if is_region(cat):
        return is_spec(text)
    else:
        return is_region(text) or is_spec(text)


def get_pageid(ls):
    search_titles = "|".join(ls)
    search_titles = search_titles.replace("&", "%26")
    pageurl = "https://en.wikipedia.org/w/api.php?action=query&format=json&titles=" + search_titles
    f = requests.get(pageurl)
    content = f.text
    pageids = re.findall(r"pageid.:(.*?)[,}]", content)
    return pageids


def wikisearch(keyword):
    base = "https://en.wikipedia.org/w/api.php?action=query&srlimit=200&list=search&format=json&srsearch=" + keyword
    f = requests.get(base)
    content = f.text
    suggest = re.findall(r"suggestion.:\"(.*?)\"[,}]", content)
    if suggest:
        suggestion = suggest[0]
        print(suggestion)
        return wikisearch(suggestion)

    titles = re.findall (r"title.:\"(.*?)\"[,}]", content)

    wordcount = re.findall(r"wordcount\":(.*?)[,}]", content)
    snippets = re.findall(r"snippet\":(.*?)\"[,}]", content)
    snippets = [re.sub(r"<[^>]*>", "", s) for s in snippets]

    combined = list(zip(titles, wordcount, snippets))
    titles = [x[0] for x in combined if int(x[1]) > 1000] #and not to_exclude(keyword, x[0], x[2])]
    total_ls = []

    for i in range(int(math.ceil(len(titles) / 40))):
        ls = []
        for j in range(0, 40):
            index = i * 40 + j
            if index >= len(titles):
                break
            ls.append(titles[index])
        total_ls.append(ls)
    total_pageids = []
    for ls in total_ls:
        ids = get_pageid(ls)
        total_pageids += ids
    return [titles, total_pageids]



def generate(outfile, to=len(search_terms)):
    df = pd.DataFrame({"terms": [""] * to, "titles": [[]] * to, "pageids": [[]] * to})
    for i in range(0, to):
        print(search_terms[i])
        search_results = wikisearch(search_terms[i])
        cur_titles = search_results[0]
        cur_pageid = search_results[1]
        print(search_results)
        df.set_value(i, "terRms", search_terms[i])
        df.set_value(i, "titles", cur_titles)
        df.set_value(i, "pageids", cur_pageid)

    df.to_csv(outfile)

# generate("data.csv", 1194)
