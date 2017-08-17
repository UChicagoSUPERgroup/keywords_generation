from read_text import get_text_from_url
import pandas as pd

def plain_match(text, location):
    score = 0
    for word in text:
        if word in location:
            score += 1

    return score / len(location)


def get_best_score(url, infile):
    text = get_text_from_url(url)
    print(text)
    with open(infile, "r") as f:
        data = f.read().split("\n")

    cat = [cat for cat in data if cat.startswith("World Localities>")]
    best_category = None
    best_score = 0
    for n in cat:
        score = plain_match(text, n)
        if score > best_score:
            best_score, best_category = score, n

    return best_category


print(get_best_score("https://www.britannica.com/place/Latin-America", "../data/interest.txt"))