import re
import time


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print('%r  %2.2f sec' % \
              (method.__name__, te - ts))
        return result

    return timed


with open("/Users/sixiongshan/Desktop/inferencing_keywords/searching/exclusion/regions.txt", 'r') as f:
    data = f.read()
data = data.split(", ")
restring = "|".join(data)


def is_region(text):
    region = re.search(restring, text)
    if region is None:
        return False
    else:
        return True


def is_spec(text):
    with open("/Users/sixiongshan/Desktop/inferencing_keywords/searching/exclusion/name.txt", 'r') as f:
        data = f.read()
    data = data.split(", ")
    with open("/Users/sixiongshan/Desktop/inferencing_keywords/searching/exclusion/exclude_ls.txt", 'r') as f:
        data2 = f.read()

    ap = ["\.com", "\.net", "Inc\."]
    data += data2.split(", ") + ap

    rstring = '|'.join(data)

    region = re.search(rstring, text)
    if region is None:
        return False
    else:
        return True
