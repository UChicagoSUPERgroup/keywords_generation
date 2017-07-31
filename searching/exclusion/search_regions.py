import re
import time
import os

def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print('%r  %2.2f sec' % \
              (method.__name__, te - ts))
        return result

    return timed


def preprocess(text):
    '''Get only Captial Letters from the text'''
    caps = re.findall(r"[A-Z][a-z]+", text)
    caps = [word for word in caps if len(word) > 2]
    text = " ".join(caps)
    text = text.strip()
    return text

with open(os.path.join(os.path.dirname(__file__), "regions.txt"), 'r') as f:
    data = f.read()
    data = data.split(", ")
    restring = "|".join(data)

def is_region(text):
    '''Search through the text for max two words'''

    text = preprocess(text)

    ls = text.split(" ")
    i = 0
    while True:
        if i >= len(ls):
            break

        if i <= len(ls) - 2:

            two_combined = " ".join([ls[i], ls[i + 1]])
            st = two_combined + "|"
            if st in restring:
                return True

        st = ls[i] + "|"
        if st in restring:
            return True

        i += 1

    return False


with open(os.path.join(os.path.dirname(__file__), "name.txt"), 'r') as f:
    names = f.read()

restring_name = "|".join(names.split(", "))

with open(os.path.join(os.path.dirname(__file__), "exclude_ls.txt"), 'r') as f:
    data2 = f.read()

ap = ["\.com", "\.net", "Inc\."]
data = data2.split(", ") + ap

rstring = '|'.join(data)


def is_spec(text):

    name_text = preprocess(text).split(" ")

    for word in name_text:

        word = "|" + word + "|"
        if word in restring_name:
            return True

    spec = re.search(rstring, text)

    if spec is None:
        return False
    else:
        return True
