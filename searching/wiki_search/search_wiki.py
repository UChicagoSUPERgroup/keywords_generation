import re
import requests
import math
import pandas as pd

'''import search terms'''
from ..search_term import get_items

'''Import exclusion Function from the exclusion package'''
from ..exclusion.search_regions import is_region, is_spec

search_terms = get_items("../health.txt")


def to_exclude(cat, title, snippet, region=True):
    '''The Exclude Function that exclude wikipedia page,
    base on the title of the page and its snippets'''

    all_letter = re.findall(r"[a-zA-Z ]+", title)

    '''Check whether there is special characters in the title 
    of the page. If so, exclude the page'''

    if len(all_letter) > 1:
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
    if is_region(cat):
        return is_spec(text)
    else:
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


def wikisearch(keyword, exclude=True):
    ''' Get a list of the wikipedia pages from
    searching the one category, and cut the unrelated '''

    '''
    Make a query to the wikipedia API
    '''

    base = "https://en.wikipedia.org/w/api.php?action=query&srlimit=200&list=search&format=json&srsearch=" + keyword
    f = requests.get(base)
    content = f.text

    '''
    If there is a suggested search in the html, extract the suggestion title, and search the suggestion instead
    '''

    suggest = re.findall(r"suggestion.:\"(.*?)\"[,}]", content)
    if suggest:
        suggestion = suggest[0]
        print(suggestion)
        return wikisearch(suggestion)

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
    if exclude:
        titles = [x[0] for x in combined if int(x[1]) > 200 and not to_exclude(keyword, x[0], x[2])]
    else:
        titles = [x[0] for x in combined if int(x[1]) > 200]
    total_ls = []

    '''
    Because the API limited the amount of page query to 50, seperate all the pages
     to groups of 40s and preform query to get the pageid for each page
     '''

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
    if exclude and len(titles) < 5:
        return wikisearch(keyword, exclude=False)

    return [titles, total_pageids]


def generate(outfile, to=len(search_terms)):
    '''Generate a outfile of all pageids for each category'''

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


generate("data.csv")
