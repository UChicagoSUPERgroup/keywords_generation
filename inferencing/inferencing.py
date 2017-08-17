from key.tree_implement import build_category_tree, print_tree, to_list, count_tree
from read_text import get_text_from_url
import pandas as pd
import math
import json
import os
from nltk.stem import SnowballStemmer
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


# t = build_category_tree("category/categories_20.json")


def find_best_category(url, t):
    text = get_text_from_url(url)

    return find_best_tree(text, t)


def save_test(infile, outfile):
    df = pd.DataFrame(pd.read_csv(infile))
    whole_ls = []
    for i in range(0, len(df['url'])):

        cur_text = get_text_from_url(df["url"][i])

        if cur_text is None:
            continue
        whole_ls.append([df["url"][i], df["category"][i], cur_text])
        print(cur_text)
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
            print("error")
            continue
        result_path = get_path(t, match_category)[1:]
        predict_path = predict.split(">")

        score = compare_score(result_path, predict_path)
        if score > 0:
            score = 1
        print(match_category, score)
        total_score += score

    return total_score


# print(test("more_text.json", "categories.json", 500))


def stem(infile, outfile):
    stemmer = SnowballStemmer("english")
    try:
        df = pd.DataFrame(pd.read_json(infile))
    except:
        df = pd.DataFrame(pd.read_csv(infile))
    # whole_ls = []
    for i in range(0, len(df["category"])):
        keywords = df['keywords'][i]
        new_keywords = [stemmer.stem(word) for word in keywords]
        new_keywords = list(set(new_keywords))
        print(len(keywords), len(new_keywords))

        df.set_value(i, "keywords", new_keywords)

    df.to_json(outfile)


def stem_all(indir, outdir):
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    for file in os.listdir(indir):
        if "json" not in file:
            continue
        file_path = indir + "/" + file
        out_path = outdir + "/" + file
        try:
            stem(file_path, out_path)
        except:
            continue


stem_all("category", "stemed_keywords")