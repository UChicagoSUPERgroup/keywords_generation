import re
import os
from re_search import timeit
import json

def splice(ls, mount):
    total_ls = []
    i = 0
    while i < len(ls):
        start = i
        end = i + mount
        l_cur = ls[start:end]
        total_ls.append(l_cur)
        i += mount
    return total_ls


@timeit
def seperate_file(infile):
    with open(infile, "r") as f:
        data = f.read()
    n_pages = re.finditer(r"doc id=.(.*?). ", data)
    indices = [x.start(0) - 1 for x in n_pages]
    parts = splice(indices, 200)
    for interval in parts:
        cur = data[interval[0]:interval[-1]]
        a = re.search(r"doc id=.(.*?). ", cur)
        if a is None:
            continue
        article_id = cur[a.start() + 8: a.end() - 2]

        with open("data/wikicorpse/" + article_id + '.txt', 'w') as f:
            f.write(cur)


def seperate_all(dir):
    for file in os.listdir(dir):
        seperate_file(dir + '/' + file)


# seperate_all("data/AB")
# seperate_all("data/AC")

file_list = []
for file in os.listdir('data/wikicorpse'):

    file_id = file.split(".")[0]
    try:
        file_list.append(int(file_id))
    except ValueError:
        continue
file_list.sort()
j = json.dumps(file_list)
with open("id_data.json", "w") as f:
    f.write(j)
