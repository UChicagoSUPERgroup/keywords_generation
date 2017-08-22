import re
from extract.keywords import extract
import bisect
import pandas as pd

''' Read id_data'''
file_list = pd.DataFrame(pd.read_json("id_data.json"))
file_list.columns = ["ids"]
file_list = file_list["ids"].tolist()


def get_text(pageid, file):
    '''Get the text of a pageid from the file that the page is in, using regular expression.
    Could use BeautifulSoup parser, which is slower for big file'''

    with open(file, "r") as myfile:
        data = myfile.read()
    a = re.search(r"id=." + str(pageid) + "", data)
    if a is None:  # Check if find id
        return
    data = data[a.start():]
    c = re.search(r"(>)", data)
    b = re.search(r"(</doc>)", data)
    text = data[c.start() + 1:b.start() - 1]  # Slice the text
    return text


def quick_search(pageid):
    '''Find the file that contain the wiki corpse for a given pageid'''
    if not isinstance(pageid, int):
        pageid = int(pageid)
    '''Quick search inside id list for the pageid'''
    index = bisect.bisect(file_list, pageid) - 1
    file = file_list[index]
    ex = get_text(pageid, "/Users/sixiongshan/Desktop/data/wikicorpse/" + str(file) + ".txt")
    if ex is None:
        return ""  # Return empty string if couldn't find the file
    return ex


def undup(seq):
    '''Remove duplicate while keep the list in order'''
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


def quick_search_ids(lx, n_key=1000):
    '''Extract keywords from the text with TextRank'''
    res = []
    [res.append(quick_search(int(x))) for x in lx]
    res = " ".join(res)
    ex = extract(res, n_key)
    ex = [x[0] for x in ex]
    return ex
