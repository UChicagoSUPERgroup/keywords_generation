
from collections import Counter

def checkfor_dup(infile):
    with open(infile, "r") as f:
        data = f.read().split("\n")

    ls = []
    for word in data:
        word = word.split(">")[-1]
        ls.append(word)
    print(Counter(ls))

checkfor_dup("interest.txt")