import re
from bs4 import BeautifulSoup
from http.cookiejar import LWPCookieJar
from urllib.request import Request, urlopen
from urllib.parse import quote_plus
import urllib.error
import os
import pandas as pd
import time
import math
import random
import requests

home_folder = os.getenv('HOME')
if not home_folder:
    home_folder = os.getenv('USERHOME')
    if not home_folder:
        home_folder = '.'  # Use the current folder on error.
cookie_jar = LWPCookieJar(os.path.join(home_folder, '.google-cookie'))
try:
    cookie_jar.load()
except Exception:
    pass

MAIN_URL = "https://www.google.com/search?q="


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


def get_page(url):
    request = Request(url)
    cookie_jar.add_cookie_header(request)
    request.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6)')
    response = urlopen(request)
    cookie_jar.extract_cookies(response, request)
    html = response.read()
    response.close()
    cookie_jar.save()
    with open("test.html", "w") as f:
        f.write(str(html))

    return html


def get_wiki_result(html):
    soup = BeautifulSoup(html, "lxml")
    search_result = soup.find(id='search').findAll('h3', class_="r")
    if search_result is None:
        return

    res = []
    for headline in search_result:
        page_url = headline.find("a", href=True)
        if "url?q=https://en.wikipedia.org/wiki/" in str(page_url):
            raw_title = headline.getText()
            is_comman = re.search(r"[a-z]:[A-Za-z]", raw_title)
            if not is_comman:
                title = raw_title.replace(" - Wikipedia", "")
                res.append(title)

    return res


def google_search_a_page(search_term, start):
    url = MAIN_URL + quote_plus(search_term + " Wikipedia") + "&start=" + str(start)

    html = get_page(url)
    titles = get_wiki_result(html)

    return titles


def google_search(search_term):
    titles = []
    start0 = google_search_a_page(search_term, 0)
    time.sleep(5 + random.uniform(0, 5))

    start10 = google_search_a_page(search_term, 10)
    # start20 = google_search_a_page(search_term, 20)
    titles += start0 + start10
    return titles


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
    categories = get_category(infile)
    search_terms = get_search_terms(infile)
    to = len(categories)
    df = pd.DataFrame({"category": [""] * to, "titles": [[]] * to, "pageids": [[]] * to})
    for i in range(0, to):
        try:
            search_results = get_pageid_titles(google_search(search_terms[i]))
        except urllib.error.HTTPError:
            time.sleep(30)
            search_results = get_pageid_titles(google_search(search_terms[i]))
        print(search_results)
        cur_titles = search_results[0]
        cur_pageid = search_results[1]
        # print(len(cur_titles), print(cur_pageid))

        df.set_value(i, "category", categories[i])
        df.set_value(i, "titles", cur_titles)
        df.set_value(i, "pageids", cur_pageid)

    df = df[["category", "titles", "pageids"]]

    df.to_csv(outfile)

generate("../data/interest.txt", "total_google.csv")
