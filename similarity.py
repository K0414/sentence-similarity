import sys
import jieba

quest_dict = []

def method_cosine(question):
    pass

def find_similar_questions(question):
    #return [ question ]
    return jieba.cut(question)

def load_quest_dict(filename):
    f = open(filename)
    l = f.readline()
    while l:
        quest_dict.append(l)
        l = f.readline()
    f.close()


if __name__=='__main__':

    if len(sys.argv) < 2:
        print 'Usage: python %s dictionary' % sys.argv[0]
        sys.exit(-1)

    # Load question dictionary.
    try:
        load_quest_dict(sys.argv[1])
    except IOError:
        print 'Open dictionary file failed.'
        sys.exit(-1)

    while True:
        question = raw_input('Input your question: ')
        candidates = find_similar_questions(question)
        for c in candidates:
            print c
