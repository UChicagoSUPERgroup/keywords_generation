import sys
import pandas
import re
import operator
import sys
sys.path.append('extract/')
from keywords import extract
from bs4 import BeautifulSoup
import bisect
import pandas as pd
import time
import math


def timeit(method):

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print('%r (%r, %r) %2.2f sec' % \
              (method.__name__, args, kw, te-ts))
        return result

    return timed


df = pd.DataFrame(pd.read_csv("first_id.csv"))


def simplify(list):
    if list[0] == 0:
        list.remove(list[0])
    res = [x for x in list if x is not None]
    return res



def search_id(pageid, file):
    with open(file, "r") as myfile:
        data = myfile.read()
    soup = BeautifulSoup(data, "html.parser")
    try:
        a = soup.find(id=pageid).getText()
    except AttributeError:
        return None
    if a == []:
        return
    return a

for i in range(0, len(df["first_id"])):
    df.set_value(i, "first_id", int(df["first_id"][i]))


def quick_search(pageid):
    position = bisect.bisect(df["first_id"], pageid)
    index = position - 1
    file = df["file"][index]
    ex = search_id(pageid, file)
    if ex == None:
        return ""
    return ex


@timeit
def quick_search_ids(lx):
    res = ""
    for x in lx:
        l = quick_search(x)
        res = res + "\n" + l
    ex = extract(res, 100)
    return ex

# def indics(list, value):
#     l = []
#     for i, j in enumerate(list):
#         if j == value:
#             l.append(i)
#     return l
#



# def unduplicates(lx):
#     lx = simplify(lx)
#     name_list = ([x[0] for x in lx])
#     value_list = ([x[1] for x in lx])
#     new_name_list = name_list
#     new_value_list = value_list
#     for name in name_list:
#         index = indics(new_name_list, name)
#         index_len = len(index)
#         save_index = index[0]
#         for j in range(1, index_len):
#             cur_index = index[j]
#             new_name_list[cur_index] = ""
#             new_value_list[save_index] += new_value_list[cur_index]
#             new_value_list[cur_index] = 0
#     new_name_list = [x for x in new_name_list if x != ""]
#     new_value_list = [x for x in new_value_list if x != 0]
#     res = list(zip(new_name_list, new_value_list))
#     return res



#
# @timeit
# def quick_search_ids(lx):
#     res = []
#     for x in lx:
#         try:
#             l = quick_search(x)
#             res = res + l
#         except TypeError:
#             res.append(l)
#     res = sorted(res, key=lambda y: y[1], reverse=True)
#     return res
#
# # def check(tuple):
#     name_list = ([x[0] for x in tuple])
#     l1 = set(name_list)
#     l1 = list(l1)
#     len1 = len(l1)
#     len2 = len(name_list)
#     return len1 == len2