import ast
import json
import re
import os
import pandas as pd
from re_search import quick_search_ids, quick_search


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

        keywords = quick_search_ids(ids)
        keywords = [key for key in keywords if is_english(key)]
        print(keywords[:50])

        cur_ls = [cat[i], keywords]

        whole_ls.append(cur_ls)

    df_out = pd.DataFrame(whole_ls, columns=["category", "keywords"])
    df_out.to_csv(outfile)


# get_keywords("total_wikipedia_20.csv", "total_keyword_new.csv")
# get_keywords("total_wiki.csv", "total_keyword_wikipage.csv")
# get_keywords("total_wikipedia_articles_60.csv", "total_keyword_wikipage_60.csv")
# get_keywords("total_wikipedia_articles_80.csv", "total_keyword_wikipage_80.csv")
# get_keywords("total_wikipedia_articles_100.csv", "total_keyword_wikipage_100.csv")

def post_process(infile, outfile):
    df = pd.DataFrame(pd.read_csv(infile))

    for i in range(0, len(df['keywords'])):
        keyword = ast.literal_eval(df['keywords'][i])

        print(i)

        df.set_value(i, 'keywords', keyword)
    df = pd.DataFrame({"category": df['category'], "keywords": df['keywords']})

    whole_ls = []

    for i in range(0, len(df['keywords'])):
        print(i)
        cur_dir = {"category": df['category'][i], "keywords": df['keywords'][i]}
        whole_ls.append(cur_dir)
    with open(outfile, "w") as f:
        json.dump(whole_ls, f)


post_process("total_keyword_new.csv", "tree_implement/total_keyword_new.csv.json")


# post_process("total_keyword_wikipage_60.csv", "tree_implement/keywords_60.json")


def get_text_files(infile, outdir):
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    with open("../data/interest.txt", 'r') as f:
        cat = f.read()

    cat = [word for word in cat.split('\n') if word is not ""]

    df = pd.DataFrame(pd.read_csv(infile))
    for i in range(0, len(df['pageids'])):
        print(cat[i])

        cur_dir = outdir + "/" + cat[i]
        if not os.path.exists(cur_dir):
            os.makedirs(cur_dir)

        ids = ast.literal_eval(df['pageids'][i])
        ids = [int(x) for x in ids]

        for id in ids:
            cur_text = quick_search(id)

            with open(cur_dir + "/" + str(id), "w") as f:
                f.write(cur_text)


                # get_text_files("combined.csv", "article_files")
