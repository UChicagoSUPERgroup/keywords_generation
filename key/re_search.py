import re
import sys
import os
import json

sys.path.append('extract/')
from keywords import extract
import bisect
import pandas as pd
import time



def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print('%r (%r, %r) %2.2f sec' % \
              (method.__name__, args, kw, te - ts))
        return result

    return timed


file_list = pd.DataFrame(pd.read_json("id_data.json"))
file_list.columns = ["ids"]
file_list = file_list["ids"].tolist()


def get_text(pageid, file):
    with open(file, "r") as myfile:
        data = myfile.read()
    id_str = r"id=." + str(pageid) + ""
    a = re.search(id_str, data)
    if a is None:
        return
    data = data[a.start():]
    c = re.search(r"(>)", data)
    b = re.search(r"(</doc>)", data)
    text = data[c.start() + 1:b.start() - 1]
    return text


def simplify(list):
    if list[0] == 0:
        list.remove(list[0])
    res = [x for x in list if x is not None]
    return res


# @timeit
def quick_search(pageid):
    try:
        pageid = int(pageid)
    except TypeError:
        pass
    position = bisect.bisect(file_list, pageid)
    index = position - 1
    file = file_list[index]
    ex = get_text(pageid, "data/wikicorpse/" + str(file) + ".txt")
    if ex is None:
        return ""
    return ex



def quick_search_ids(lx, n_key=100):
    res = []
    for x in lx:
        x = int(x)
        l = quick_search(x)
        res.append(l)
    res = " ".join(res)
    ex = extract(res, n_key)
    ex = [x[0] for x in ex]
    return ex

