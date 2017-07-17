from re_search import quick_search_ids
import pandas as pd
import sys
import re
import ast
import json

sys.path.append("/Users/sixiongshan/Desktop/inferencing_keywords/searching")
from searching.search_wiki import wikisearch


# from searching.search_wiki import wikisearch

#
# def search_category(category, n_key=100):
#     result = wikisearch(category)
#     keywords = quick_search_ids(result, n_key)
#     return keywords
#
#
# # print(search_category("arts"))
#
#
#
#
#
# def save(outfile, infile="interest.txt"):
#     search_items = get_items(infile)
#     df = pd.DataFrame({"category": [""] * 2100, "keywords": [[]] * 2100})
#     for i in range(0, len(search_items)):
#         df.set_value(i, "category", search_items[i])
#         keywords = search_category(search_items[i])
#         print(keywords)
#         df.set_value(i, "keywords", keywords)
#
#     df.to_csv(outfile)


# save("interest.txt", "test.csv")

# def test_search(outfile, infile="interest.txt"):
#     search_items = get_items(infile)
#     df = pd.DataFrame({"category": [""] * 2100, "pages": [[]] * 2100})
#     for i in range(0, 1500, 30):
#         print(i)
#         df.set_value(i, "category", search_items[i])
#         pages = wikisearch(search_items[i])
#         df.set_value(i, "pages", pages)
#     df.to_csv(outfile)
#
# test_search("page_test.csv")


def push_blank(infile, outfile):
    df = pd.DataFrame(pd.read_csv(infile))
    for i in range(0, len(df["keywords"])):
        cur_keywords = ast.literal_eval(df["keywords"][i])
        if cur_keywords == []:
            print(df["category"][i])
            # term = df["category"][i].split(">")[-1].replace("&", "and")
            # print(term)
            #
            # ids = wikisearch(term)[:10][1]
            #
            # keywords = quick_search_ids(ids)
            # print(keywords)
            # df.set_value(i, "keywords", keywords)
            # df.to_csv("test.csv")
            # df.to_json(outfile)


# push_blank("keywords_test.csv", "keywords_test.json")



def get_keywords(infile, outfile):
    with open("interest.txt", 'r') as f:
        cat = f.read()
    cat = [word for word in cat.split('\n') if word is not ""]
    whole_ls = []
    df = pd.DataFrame(pd.read_csv(infile))
    for i in range(0, len(df['pageids'])):
        ids = ast.literal_eval(df['pageids'][i])
        ids = [int(x) for x in ids]

        keywords = quick_search_ids(ids, 100)

        cur_ls = [cat[i], keywords]

        whole_ls.append(cur_ls)

    df_out = pd.DataFrame(whole_ls, columns=["category", "keywords"])
    df_out.to_csv("keywords_test.csv")


# get_keywords("data.csv", "")
def is_english(word):
    match = re.findall(r'[A-Za-z ]', word)
    if len(match) == len(word):
        return True
    else:
        return False


def post_process(infile, outfile):
    df = pd.DataFrame(pd.read_csv(infile))

    for i in range(0, len(df['keywords'])):
        keyword = ast.literal_eval(df['keywords'][i])

        keyword = [word for word in keyword if is_english(word)]
        print(i)

        df.set_value(i, 'keywords', keyword)
    df = pd.DataFrame({"category": df['category'], "keywords": df['keywords']})
    whole_ls = []
    for i in range(0, len(df['keywords'])):
        cur_dir = {"category": df['category'][i], "keywords": df['keywords'][i]}
        whole_ls.append(cur_dir)
    with open("keywords.json", "w") as f:

        json.dump(whole_ls, f)

    # df.to_json(outfile)




post_process("keywords_test.csv", "keywords.json")