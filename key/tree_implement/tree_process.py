from remove_duplicate import remove_duplicate_2
from tree_struct import Node, build_category_tree, print_tree, to_list, count_tree
import pandas as pd
import json

import math


def print_two_trees(tree1, tree2):
    if tree1 is None or tree2 is None:
        return

    print(tree1.category, tree2.category)
    for c1, c2 in zip(tree1.children, tree2.children):
        print_two_trees(c1, c2)


def remove_duplicate_tree(t):
    if t is None:
        return

    children_ls = []

    for child in t.children:
        children_ls.append(child.keywords)
    children_ls = remove_duplicate_2(children_ls)

    for i, child in enumerate(t.children):
        child.keywords = children_ls[i]
        # print(len(child.keywords))

    for child in t.children:
        remove_duplicate_tree(child)

    return t


def post_process(infile, outfile):
    df = pd.DataFrame(pd.read_json(infile))
    category = df['category']
    keyword_ls = df['keywords']
    print(len(keyword_ls))

    t = build_category_tree(infile)

    keyword_ls = to_list(t)[1:]
    print(len(keyword_ls))




    #
    # df = pd.DataFrame({"category": category, "keywords": keyword_ls})
    #
    # whole_ls = []
    # for i in range(0, len(category)):
    #     print(i)
    #     cur_dir = {"category": df['category'][i], "keywords": df['keywords'][i]}
    #     whole_ls.append(cur_dir)
    #
    # with open(outfile, "w") as f:
    #     json.dump(whole_ls, f)

# post_process("keywords.json",
#              "/Users/sixiongshan/Desktop/GitHub/trackingtransparency/extension/lib/inferencing_data/categories.json")
