import sys
import jieba
import operator
import math

doc_dict = []
doc_vectors = []
dfs = {}

def calc_df(documents):
    for d in documents:
        for w in set(d):
            if w not in dfs:
                dfs[w] = 1
            else:
                dfs[w] += 1

def method_cosine(question):
    # 1. Word segmentation and stop words filtering.
    # 2. Extract descriptive words using tf-idf.
    # 3. Build vectors for question and each sentence in dictionary.
    # 4. Calculate cosine distance.
    # 5. Get TopK candidates.
    pass

def method_bm25(question):
    def idf(word):
        df = (word in dfs) and dfs[word] or 0.0
        return math.log((len(doc_dict) - df + 0.5) / (df + 0.5))

    def bm25(quest, doc, K1=2.0, b=0.75):
        tf = {}
        for w in quest:
            tf[w] = 0.0
        for w in doc:
            if w in tf:
                tf[w] += 1.0
        bm25 = 0.0
        for k in tf.keys():
            bm25 += idf(k) * (tf[k] * (K1 + 1)) / (tf[k] + K1 * (1 - b + b * len(doc) / avgdl))
        return bm25

    # 1. Calculate avgdl.
    totdl = 0.0
    for d in doc_vectors:
        totdl += len(d)
    avgdl = totdl / len(doc_vectors)
    # 2. Calculate BM25 for each document.
    scores = {}
    quest_vector = [x for x in jieba.cut(question)]
    for idx, doc in enumerate(doc_vectors):
        scores[idx] = bm25(quest_vector, doc)
    # 3. Get Top5 candidates.
    candidates = sorted(scores.iteritems(), key=operator.itemgetter(1))[-5:]
    return candidates[::-1]

def method_tfidf(question):
    def tfidf(quest, doc):
        tf = {}
        for w in quest:
            tf[w] = 0.0
        for w in doc:
            if w in tf:
                tf[w] += 1.0
        tfidf = 0.0
        for k in tf.keys():
            df = (k in dfs) and dfs[k] or 0.0
            tfidf += (tf[k] / len(doc)) * math.log(len(doc_dict) / (1 + df))
        return tfidf
    # 1. Word segmentation and stop words filtering.
    quest_vector = [x for x in jieba.cut(question)]
    # 2. Calculate tfidf for each document.
    tfidfs = {}
    for idx, doc in enumerate(doc_vectors):
        tfidfs[idx] = tfidf(quest_vector, doc)
    # 3. Get Top5 candidates.
    candidates = sorted(tfidfs.iteritems(), key=operator.itemgetter(1))[-5:]
    return candidates[::-1]

def find_similar_questions(question):
    #return method_tfidf(question)
    return method_bm25(question)

def load_doc_dict(filename):
    f = open(filename)
    l = f.readline()
    while l:
        doc_dict.append(l)
        l = f.readline()
    f.close()


if __name__=='__main__':

    if len(sys.argv) < 2:
        print 'Usage: python %s dictionary' % sys.argv[0]
        sys.exit(-1)

    # Load question dictionary.
    try:
        load_doc_dict(sys.argv[1])
    except IOError:
        print 'Open dictionary file failed.'
        sys.exit(-1)

    # Cut sentences into word vectors.
    for q in doc_dict:
        doc_vectors.append([ x for x in jieba.cut(q)])

    # Calculate DF of each word in the dictionary.
    calc_df(doc_vectors)

    while True:
        question = raw_input('Input your question: ')
        candidates = find_similar_questions(question)
        for i, c in enumerate(candidates):
            print 'Doc%d: %f, %s' % (i+1, c[1], doc_dict[c[0]])
