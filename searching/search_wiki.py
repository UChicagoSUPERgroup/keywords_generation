import re
import requests
import math
import pandas as pd
from timeit import timeit
from urllib.parse import quote_plus
from exclusion.search_regions import is_region, is_spec
# from nltk.stem import WordNetLemmatizer


# def singular(words):
#     '''
#     Get the singular version of a list of words with NLTK lemmatizer
#     '''
#
#     wnl = WordNetLemmatizer()
#     words = words.split(" ")
#     ls = []
#     for word in words:
#         if word.isupper():
#             ls.append(word)
#         else:
#             ls.append(word.lower())
#
#     words = [wnl.lemmatize(word) for word in ls]
#     words = " ".join(words)
#
#     return words


def uncode(code):
    code = bytes(code, encoding='utf-8')
    return code.decode('unicode-escape')


def to_exclude(title, snippet, region=True):
    '''The Exclude Function that exclude wikipedia page,
    base on the title of the page and its snippets'''

    '''Check whether there is special characters in the title 
    of the page. If so, exclude the page'''

    all_letter = re.findall(r"[a-zA-Z0-9\u00E0-\u00FC ]", title)

    if len(all_letter) != len(title):
        return True

    '''Check whether the title is a list of things'''

    is_ls = re.search("([Ll]ist)", title)

    if is_ls is not None:
        return True

    '''Combined the title and snippet to 
    preform region exclusion'''

    text = " ".join([title, snippet])

    if not region:
        return is_spec(text)

    '''If the category is not region, then get rid of all text that contain regions'''

    return is_region(text) or is_spec(text)


def get_pageid(ls):
    '''Function to get wikipedia pageid from title name'''

    '''Join all titles together'''
    search_titles = "|".join(ls)

    search_titles = search_titles.replace("&", "%26")  # Ready for html input

    '''Generate wikipedia query url'''
    pageurl = "https://en.wikipedia.org/w/api.php?action=query&format=json&titles=" + search_titles
    f = requests.get(pageurl)
    content = f.text

    '''Extract all the pageid from the json output of the html'''
    pageids = re.findall(r"pageid.:(.*?)[,}]", content)

    return pageids


@timeit
def wikisearch(keyword, exclude=True, exclude_region=True):
    ''' Get a list of the wikipedia pages from
    searching the one category, and cut the unrelated '''

    '''
    Make a query to the wikipedia API
    '''

    base = "https://en.wikipedia.org/w/api.php?action=query&srlimit=500&list=search&format=json&srsearch=" + keyword

    f = requests.get(base)
    content = f.text

    '''
    If there is a suggested search in the html, extract the suggestion title, and search the suggestion instead
    '''

    suggest = re.findall(r"suggestion.:\"(.*?)\"[,}]", content)

    if suggest:
        suggestion = suggest[0]
        print("Suggestion:", suggestion)
        return wikisearch(suggestion, exclude=exclude, exclude_region=exclude_region)

    '''
    Get the title, wordcount, and snippets of each wikipedia article
    '''

    titles = re.findall(r"title.:\"(.*?)\"[,}]", content)

    wordcount = re.findall(r"wordcount\":(.*?)[,}]", content)
    snippets = re.findall(r"snippet\":(.*?)\"[,}]", content)
    snippets = [re.sub(r"<[^>]*>", "", s) for s in snippets]  # Get text from the snippets

    combined = list(zip(titles, wordcount, snippets))

    '''
    Preform exclusion on the pages
    '''

    if exclude and exclude_region:
        titles = [x[0] for x in combined if not to_exclude(x[0], x[2])]

    elif exclude and not exclude_region:

        titles = [x[0] for x in combined if not to_exclude(x[0], x[2], region=False)]

    else:

        titles = [x[0] for x in combined]

    '''If the result is less than 5 pages, turn off the exclude function'''
    print(len(titles))
    if exclude and len(titles) < 5:
        print("not exclude")
        return wikisearch(keyword, exclude_region=exclude_region, exclude=False)

    titles = titles[:20]

    for i, title in enumerate(titles):
        if "\\" in title:
            titles[i] = uncode(title)

    return titles


def get_pageid_titles(titles):

    '''
    Because the API limited the amount of page query to 50, seperate all the pages
     to groups of 40s and preform query to get the pageid for each page
     '''

    total_ls = []

    for i in range(int(math.ceil(len(titles) / 49))):
        ls = []
        for j in range(0, 49):
            index = i * 49 + j
            if index >= len(titles):
                break
            ls.append(titles[index])
        total_ls.append(ls)
    total_pageids = []

    for ls in total_ls:
        ids = get_pageid(ls)
        total_pageids += ids

    return [titles, total_pageids]


# def get_search_terms(infile):
#     with open(infile, "r") as f:
#         categories = f.read().split("\n")
#
#     new_category = []
#     for word in categories:
#
#         word = word.split(">")[-1]
#         word = singular(word)
#         word = word.split(" ")
#
#         word = " ".join([x[0].upper() + x[1:] for x in word]).replace("&", "and")
#
#         new_category.append(word)
#
#     return new_category

def get_search_terms(infile):
    with open(infile, "r") as f:
        categories = f.read().split("\n")

    new_category = []
    for word in categories:
        word = word.split(">")[-2:]
        combined = " ".join(word)

        new_category.append(combined)

    return new_category


def get_category(infile):
    with open(infile, "r") as f:
        categories = f.read().split("\n")
    return categories


def generate(infile, outfile):
    '''Generate a outfile of all pageids for each category'''

    categories = get_category(infile)
    search_terms = get_search_terms(infile)
    to = len(categories)
    print(to)
    df = pd.DataFrame({"category": [""] * to, "titles": [[]] * to, "pageids": [[]] * to})
    for i in range(0, to):
        print(search_terms[i])

        if is_region(categories[i]) or "ocalities" in categories[i]:
            print("region")
            search_results = get_pageid_titles(wikisearch(quote_plus(search_terms[i]), exclude_region=False))

        else:

            search_results = get_pageid_titles(wikisearch(quote_plus(search_terms[i])))

        cur_titles = search_results[0]
        cur_pageid = search_results[1]
        print(search_results)

        df.set_value(i, "category", categories[i])
        df.set_value(i, "titles", cur_titles)
        df.set_value(i, "pageids", cur_pageid)

    df = df[["category", "titles", "pageids"]]

    df.to_csv(outfile)


generate("../data/interest.txt", "total_wikipedia_articles_100.csv")