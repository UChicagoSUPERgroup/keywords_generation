import operator
import sys
import re
import nltk
from nltk import word_tokenize, pos_tag, corpus
# from nltk.stem.porter import PorterStemmer
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import networkx as nx
from bs4 import BeautifulSoup


def extract(txt, num):
    # initialize stemmer
    # stemmer = PorterStemmer()
    stemmer = SnowballStemmer('english')

    # stem text and tokenize words
    tokens = [
        w
        for w in word_tokenize(stemmer.stem(txt))
        if w not in stopwords.words('english') and w != "–"
    ]

    # part of speech tags
    pos_tokens = pos_tag(tokens)

    # only keep nouns and adjectives to extract nodes
    filtered_tokens = [
        x[0] for x in pos_tokens
        if x[1].startswith("N") or x[1].startswith("J")
    ]
    filtered_tokens = [stemmer.stem(token) for token in filtered_tokens]

    # cleaned_tokens = [
    #        t[0] 
    #        for t in pos_tokens if re.search("[A-Za-z]", t[1]) is not None
    # ]

    # initialize graph
    g = nx.Graph()

    # add nodes to graph
    g.add_nodes_from(filtered_tokens)

    # generate edges
    edges = []
    for i, t in enumerate(filtered_tokens):
        first = t
        try:
            second = filtered_tokens[i + 1]
        except:
            break

        edges.append((t, second))

        try:
            third = filtered_tokens[i + 2]
        except:
            break

        edges.append((t, third))

    # add edges to graph
    g.add_edges_from(edges)

    # rank edges
    scores = nx.pagerank(g, max_iter=25, tol=.0001)
    # scores = nx.hits(g)[0]

    # sort scores
    sorted_scores = sorted(
        scores.items(),
        key=operator.itemgetter(1),
        reverse=True,
    )

    return sorted_scores[:num]


# for s in extract(txt):
#    print("{0: <16}  | Score: {1:.4f}".format(s[0], s[1])) 

'''
vectorizer = TfidfVectorizer("")

def extract(txt):
    # tokenize and apply part of speech tags
    words = word_tokenize(txt)    
    tagged_words = pos_tag(words)

    # apply syntactic filter (nouns and adjectives)
    filtered_words = [
        x[0] for x in tagged_words
        if x[1].startswith("N") or x[1].startswith("J")
    ]

    # generate vertex matrix
    matrix = vectorizer.fit_transform(filtered_words)
    matrix = matrix * matrix.transpose()

    # add to graph, edge added through co-occurrence
    # edge weight defaults to one
    graph = nx.from_scipy_sparse_matrix(matrix)

    # apply pagerank algorithm to rank vertices
    scores = nx.pagerank_scipy(graph, max_iter=100)

    # sort vertices in decreasing order and pick out the 
    # first n terms
    pagerank = sorted(scores.items(), key=operator.itemgetter(1),
            reverse=True)[:50]
    print(pagerank)
    summary_indexes = sorted(pagerank)
    keywords = [filtered_words[i] for i, score in summary_indexes]
   
    # TODO: multiword support

    return keywords
'''


def extract_wiki_xml(filename):
    with open(filename) as f:
        data = f.read()

    soup = BeautifulSoup(data, "html.parser")

    ls = soup.find_all("doc")

    for article in ls:
        print("\n" + article["title"])
        for s in extract(article.text):
            print("{0: <16}  | Score: {1:.4f}".format(s[0], s[1]))

            # extract_wiki_xml("wiki_00.xml")
