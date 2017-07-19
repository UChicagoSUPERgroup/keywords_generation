import ast
import json
import re
import sys
import pandas as pd
from re_search import quick_search_ids


def is_english(word):
    match = re.findall(r'[A-Za-z]', word)
    if len(match) == len(word):
        return True
    else:
        return False


def get_keywords(infile, outfile):
    with open("../data/interest.txt", 'r') as f:
        cat = f.read()
    cat = [word for word in cat.split('\n') if word is not ""]
    whole_ls = []
    df = pd.DataFrame(pd.read_csv(infile))
    for i in range(0, len(df['pageids'])):
        print(cat[i])
        ids = ast.literal_eval(df['pageids'][i])
        ids = [int(x) for x in ids]

        keywords = quick_search_ids(ids, 120)
        keywords = [key for key in keywords if is_english(key)]
        print(keywords)

        cur_ls = [cat[i], keywords[:100]]

        whole_ls.append(cur_ls)

    df_out = pd.DataFrame(whole_ls, columns=["category", "keywords"])
    df_out.to_csv(outfile)


get_keywords("total_pageids.csv", "total_keywords.csv")




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

            # df.to_csv(outfile)


# post_process("keywords_test.csv", "keywords.json")
