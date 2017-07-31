from key.tree_implement import build_category_tree, print_tree, to_list, count_tree
import math
from read_text import get_text_more
import pandas as pd


def print_tree2(t):
    def print_helper(tree, depth):

        c_len = len(tree.children)
        for i in range(0, int(c_len / 2)):
            print_helper(tree.children[i], depth + len(tree.category))

        print("{0}{1}".format(" " * (depth + 2), tree.category))

        for i in range(int(c_len / 2), c_len):
            print_helper(tree.children[i], depth + len(tree.category))

    print_helper(t, 0)


# t = build_category_tree("categories.json")


# print_tree2(t)

# @timeit
def get_path(tr, cat):
    stack = []

    def _getpath(head):
        nonlocal stack
        nonlocal cat

        if head.category == cat:
            stack.append(head.category)
            return True
        for c in head.children:

            if _getpath(c):
                stack.append(head.category)
                return True

        return False

    _getpath(tr)
    return list(reversed(stack))


def compare_score(result, predict):
    # total_length = min(len(predict), len(result))
    # print(total_length)
    # i = 0
    # for i in range(0, total_length):
    #     print(i)
    #     if result[i] != predict[i]:
    #         break
    #
    # score = (i + 1) / total_length
    #
    result_length = len(result)
    predict_length = len(predict)

    score = len(set(result) & set(predict)) / predict_length

    return score