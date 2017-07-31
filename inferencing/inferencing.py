from key.tree_implement import build_category_tree, print_tree, to_list, count_tree
from read_text import get_text_more, get_text
import pandas as pd
import math
from tree_comparsion import compare_score, get_path
import matplotlib.pyplot as plt


def match(text, keywords, keywords_amount=1000):
    score = 0
    total_length = len(text)

    if total_length == 0:
        return 0

    for word in text:
        if word in keywords[:keywords_amount]:
            score += 1

    total_score = score / total_length
    return total_score


def find_best_tree(text, t, mount=1000):
    def find_best_children(text, t):
        if t is None:
            return

        best_score = 0
        best_child = None
        for c in t.children:
            cur_score = match(text, c.keywords, keywords_amount=mount)

            if cur_score > best_score:
                best_score = cur_score
                best_child = c

        return [best_score, best_child]

    parent_score = match(text, t.keywords, keywords_amount=mount)

    find_child = find_best_children(text, t)

    best_child_score = find_child[0]
    best_child = find_child[1]

    if parent_score > best_child_score:
        return t.category
    else:
        # print(best_child.category)
        return find_best_tree(text, best_child)

t = build_category_tree("category/categories_20.json")


def find_best_category(url, t):
    # t = build_category_tree(infile)
    text = get_text_more(url)

    return find_best_tree(text, t)
print(find_best_category("http://www.caranddriver.com/kia/soul", t))

def save_test(infile, outfile):
    df = pd.DataFrame(pd.read_csv(infile))
    whole_ls = []
    for i in range(0, len(df['url'])):
        print(i)
        cur_text = get_text_more(df["url"][i])

        if cur_text is None:
            continue
        whole_ls.append([df["url"][i], df["category"][i], cur_text])

    df = pd.DataFrame(whole_ls, columns=['url', 'category', 'text'])
    # df.to_csv("check_test.csv")
    df.to_json(outfile)


# save_test("test_set.csv", "more_text.json")

# @timeit
def test(infile, keywords_infile, keywords_mount):
    df = pd.DataFrame(pd.read_json(infile))
    t = build_category_tree(keywords_infile)

    total_score = 0

    for i in range(0, len(df['text'])):

        text, predict = df['text'][i], df['category'][i]
        try:
            match_category = find_best_tree(text, t, keywords_mount)
        except AttributeError:
            continue
        result_path = get_path(t, match_category)[1:]
        predict_path = predict.split(">")

        score = compare_score(result_path, predict_path)
        print(score)
        total_score += score

    return total_score


# # Best = 23.3
# print(test("more_text.json", "category/categories_20.json", 500)) # 26

# print(test("more_text.json", "category/categories_80_c.json", 500))
# print(test("more_text.json", "category/categories_40_c.json", 500))  # 24
# print(test("more_text.json", "category/categories_40_cc.json", 500))  # 6.7
# print(test("more_text.json", "category/categories_60.json", 500))  # 22.8
# print(test("more_text.json", "category/categories_60_c.json", 500))  # 16.9
# print(test("more_text.json", "category/categories_60_cc.json", 500))  # 10.2


def comp(infile1, infile2):
    df1 = pd.DataFrame(pd.read_json("more_text.json"))
    df2 = pd.DataFrame(pd.read_json("test_set_save_text.json"))
    ls1 = df1['text']
    ls2 = df2['text']

    for a, b in zip(ls1, ls2):
        print(len(a), len(b))


# comp("", "")


def plot(x_axis, y_axis, outfile):
    if len(x_axis) != len(y_axis):
        plt.plot(y_axis)
    else:
        plt.plot(x_axis, y_axis)
    plt.ylabel('Keywords Score')
    plt.xlabel('Number of Keywords')
    plt.savefig(outfile)
    plt.show()


def test_keywords(infile, outfile):
    score_ls = []
    mount_ls = []
    for numbers in range(0, 500, 50):
        mount_ls.append(numbers)
        score = test("test_set_save_text.json", infile, numbers)
        print(score)
        score_ls.append(score)
    plot(mount_ls, score_ls, outfile)

# test_keywords("category/catgeories1.json", "cat1")
# test_keywords("category/catgeories2.json", "cat2")
# test_keywords("category/catgeories3.json", "cat3")
# test_keywords("category/catgeories41.json", "cat41")
# test_keywords("category/catgeories42.json", "cat42")
