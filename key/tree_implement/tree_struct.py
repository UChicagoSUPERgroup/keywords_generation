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

    print(tree.category, "  ", len(tree.keywords))
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


def build_category_tree(infile):
    """
    Assumes input file is formatted as follows:
    Category1>Category2>...>CategoryX ...
    where everything is optional (blank lines are allowed)
    """
    df = pd.DataFrame(pd.read_json(infile))

    data = df["category"]
    keywords = df["keywords"]

    # initialize tree with just a root

    tree = Node("Root")

    for i in range(0, len(data)):
        line = data[i]
        keyword_cur = keywords[i]

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


def merge_tree(tree, n_key=2000):
    if tree.children == []:
        return
    keys = []
    for c in tree.children:
        merge_tree(c)
    n_children = len(tree.children)
    for i in range(0, n_key):
        index = i % n_children
        ind = math.floor(i / n_children)
        cur = tree.children[index]
        try:
            cur_keys = cur.keywords[ind]
            keys.append(cur_keys)
        except IndexError:
            # print(ind)
            break
    s = keys
    # s = set(keys)
    # s = list(s)
    tree.keywords = s[:int(n_key)]

    return tree


def count_tree(tr):
    if tr is None:
        return
    count = 1
    # print(tr.category)
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


def merge_tree_file(infile, outfile):
    tree = build_category_tree(infile)
    df = pd.DataFrame(pd.read_json(infile))
    cat = df['category']
    tree = merge_tree(tree, 2000)
    print_tree(tree)
    df2 = pd.DataFrame({"category": cat, "keywords": to_list(tree)[1:]})
    df2.to_csv(outfile)