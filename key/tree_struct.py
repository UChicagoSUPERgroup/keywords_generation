# Building trees from category data
import pandas as pd
import math
import re
import numpy


# Node for a tree containing categories and keywords associated
# with those categories
class Node(object):
    def __init__(self, cat, keywords=[], children=[]):
        self.category = cat
        self.keywords = keywords
        self.children = children


def print_tree(tree):
    if tree is None:
        return

    print(tree.category, len(tree.keywords))
    for c in tree.children:
        print_tree(c)


def find_and_add_child(cat, child, tree):
    """
    Find given category in given tree and add a child to the
    found node. Assumes category exists and is unique.
    """
    if tree is None:
        print("doh")
    elif tree.category == cat:
        tree.children = tree.children + [child]
    else:
        for c in tree.children:
            find_and_add_child(cat, child, c)


df = pd.DataFrame(pd.read_csv("keywords_combined_300.csv"))


def build_category_tree(df):
    """
    Assumes input file is formatted as follows:
    Category1>Category2>...>CategoryX ...
    where everything is optional (blank lines are allowed)
    """
    data = df["category"]
    keywords = df["keywords"]

    # initialize tree with just a root

    tree = Node("Root")

    for i in range(0, len(data)):
        line = data[i]
        keyword_cur = keywords[i]
        keyword_cur = re.findall(r"\(.(.*?).,", keyword_cur)

        if line == "":
            continue

        categories = line.split(">")

        if len(categories) == 1:
            cat = "Root"
        else:
            cat = categories[-2]

        child = Node(categories[-1])
        child.keywords = keyword_cur
        find_and_add_child(cat, child, tree)

    return tree


tree = build_category_tree(df)
print_tree(tree)

def clean(tree):
    if tree.children != []:
        tree.keywords = []
    for c in tree.children:
        clean(c)
    return tree


# def merge_tree(tree, n_key=100):
#     if tree.children == []:
#         return
#     n_children = len(tree.children)
#     d = numpy.empty((n_children + 1, 0)).tolist()
#     d[0] = tree.keywords
#     for c in n_children:
#         merge_tree(c)
#         tree.keywords += c.keywords[:n_key]
#
#     s = set(tree.keywords)
#     s = list(s)
#     tree.keywords = s[:n_key]
#     return tree


def merge_tree(tree, n_key=500):
    if tree.children == []:
        return
    keys = []
    for c in tree.children:
        merge_tree(c)

    n_children = len(tree.children)
    for i in range(0, n_key*n_children):
        index = i % n_children
        ind = math.floor(i / n_children)
        cur = tree.children[index]
        try:
            cur_keys = cur.keywords[ind]
        except IndexError:
            print(ind)
        keys.append(cur_keys)

    s = set(keys)
    s = list(s)
    tree.keywords = s[:int(n_key / 2)] + tree.keywords[:int(n_key / 2)]

    return tree


tree = merge_tree(tree)


def count_tree(tr):
    if tr is None:
        return
    count = 1
    print(tr.category)
    for c in tr.children:
        count += count_tree(c)

    return count


def to_list(tr):
    if tr is None:
        return

    ls_keywords = [tr.keywords]
    for c in tr.children:
        ls_keywords += to_list(c)
    return ls_keywords


cat = []
for i in df["category"]:
    # try:
    #     float(i)
    # except ValueError:
    #     cat.append(i)
    cat.append(i)


def leaves(tree):
    ls = tree.keywords
    for c in tree.children:
        leaves(c)
        ls += c.keywords
    return ls


def score(tree):
    ls = leaves(tree)
    l_list = len(ls)
    ls = set(ls)
    ls = list(ls)
    l_set = len(ls)
    return 1 - ((l_list - l_set) / l_list)


def merge_tree_file(tree, outfile):
    tree = clean(tree)
    tree = merge_tree(tree, 300)
    df2 = pd.DataFrame({"Category": cat, "keywords": to_list(tree)[1:]})
    df2.to_csv(outfile)


# merge_tree_file(tree, "merge_300.csv")
