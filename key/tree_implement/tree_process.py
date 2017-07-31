from remove_duplicate import remove_duplicate_2, remove_duplicate
from tree_struct import Node, build_category_tree, print_tree, to_list, count_tree
import pandas as pd
import json
import sys

import math


def remove_duplicate_tree(t):
    if t is None:
        return

    children_ls = []

    for child in t.children:
        children_ls.append(child.keywords)
    children_ls = remove_duplicate_2(children_ls)

    for i, child in enumerate(t.children):
        child.keywords = children_ls[i]
        print(len(child.keywords))

    for child in t.children:
        remove_duplicate_tree(child)

    return t


def post_process(infile, outfile):
    df = pd.DataFrame(pd.read_json(infile))
    category = df['category']
    # keyword_ls = df['keywords']
    # print(len(keyword_ls))

    t = build_category_tree(infile)
    t = remove_duplicate_tree(t)
    keyword_ls = to_list(t)[1:]
    # print(len(keyword_ls))

    df = pd.DataFrame({"category": category, "keywords": keyword_ls})

    whole_ls = []
    for i in range(0, len(category)):
        # print(i)
        print(len(df['keywords'][i]))
        cur_dir = {"category": df['category'][i], "keywords": df['keywords'][i]}
        whole_ls.append(cur_dir)

    with open(outfile, "w") as f:
        json.dump(whole_ls, f)


# post_process("keywords_80.json", "/Users/sixiongshan/Desktop/GitHub/geosearch/keywords_generation/inferencing/category/categories_80_c.json")




# post_process("keywords.json",
#              "/Users/sixiongshan/Desktop/GitHub/trackingtransparency/extension/lib/inferencing_data/categories.json")
