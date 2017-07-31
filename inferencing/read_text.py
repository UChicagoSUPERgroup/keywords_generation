import requests
import json
from nltk.stem import WordNetLemmatizer
import urllib.request
import urllib.error
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import time


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print('%r  %2.2f sec' % \
              (method.__name__, te - ts))
        return result

    return timed
MERCURY_API = 'https://mercury.postlight.com/parser?url='


def get_text(url):
    MERCURY_API = 'https://mercury.postlight.com/parser?url='

    key = "w2K2KogZrhKJpK9Z8KxaT9yaZ52uG9zgNMZk49Ut"

    url = '{0}{1}'.format(MERCURY_API, url)
    headers = {'x-api-key': key}
    s = requests.Session()
    r = s.get(url, headers=headers)
    text = re.sub(r"<[^>]*>", "", r.text)
    d = json.loads(text)
    text = '{0} {1}'.format(d.get("title"), d.get("content"))
    text = " ".join(re.findall(r"[A-Za-z ]+", text)).lower()
    text = text.split()

    return text

print(get_text("https://www.grubhub.com/"))

# @timeit
def get_text_more(url):
    html = requests.get(url).text
    # print(html)

    html = "".join(line.strip() for line in html.split("\n"))
    extract_comments = re.sub(r"<!--(.*?)-->", "", html)
    soup = BeautifulSoup(extract_comments, "lxml")
    data = soup.findAll(text=True)

    # print(data)
    # [print(s) for s in data if s.parent.name == "p"]
    # print(set([(s.parent.name) for s in data]))
    def visible(element):
        if element.parent.name in ['style', 'script', '[document]', 'head', 'title', 'form']:
            return False
        elif re.match(r"<!--(.*?)-->", str(element.encode('utf-8'))):
            return False
        return True

    result = " ".join(filter(visible, data))
    text = " ".join(re.findall(r"[A-Za-z ]+", result)).lower()
    text = text.split()
    return text


print(len(get_text_more("https://www.cnn.com/")))


# def compare_extract(infile):
#     df = pd.DataFrame(pd.read_json(infile))
#     urls = df['url']
#     for url in urls:
#         print(url)
#         time1 = get_text(url)
#         time2 = get_text_more(url)
#         if time2 is None:
#             print("None")
#             continue
#         print(len(time1), len(time2))

# compare_extract("test_set_save_text.json")
