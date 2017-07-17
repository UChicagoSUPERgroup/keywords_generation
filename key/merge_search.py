import pandas as pd
from re_search import quick_search_ids
from tree_struct import build_category_tree, merge_tree_to_file



def merge_keywords(infile, outfile):
    # Read a csv file where Category is a column of category of ads interests, and pageid are a column of pageids
    df = pd.DataFrame(pd.read_csv(infile))
    for