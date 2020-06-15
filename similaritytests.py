from sklearn.feature_extraction.text import TfidfVectorizer
from os import listdir
from os.path import isfile, join
import difflib
import distance
import wmd
import pandas as pd
from nltk.corpus import stopwords
import nltk; nltk.download('stopwords', quiet=True)
import gensim
import spacy
from functools import wraps
from time import time

def timed(f):
  @wraps(f)
  def wrapper(*args, **kwds):
    start = time()
    result = f(*args, **kwds)
    elapsed = time() - start
    print ("%s took %d seconds to finish" % (f.__name__, elapsed))
    return result
  return wrapper

@timed
def wmv(txt1, txt2):
    stop_words = stopwords.words('english')
    doc1 = open(txt1).read()
    doc2 = open(txt2).read()
    a = doc1.lower().strip()
    b = doc2.lower().strip()
    a = [w for w in a if w not in stop_words]
    b = [w for w in b if w not in stop_words]
    model = gensim.models.KeyedVectors.load_word2vec_format('~/GoogleNews-vectors-negative300.bin', binary=True)
    thedistance = model.wmdistance(a, b)
    return thedistance

@timed
def simiemd(txt1, txt2):
    doc1 = open(txt1).read()
    doc2 = open(txt2).read()
    a = doc1.split()
    b = doc2.split()
    model = gensim.models.KeyedVectors.load_word2vec_format('~/GoogleNews-vectors-negative300.bin', binary=True)
    ourdistance = model.wmdistance(a, b)
    return ourdistance

def theearth():
    nlp = spacy.load('en_core_web_md')
    nlp.add_pipe(wmd.WMD.SpacySimilarityHook(nlp), last=True)
    doc1 = nlp("Politician speaks to the media in Illinois.")
    doc2 = nlp("The president greets the press in Chicago.")
    print(doc1.similarity(doc2))

def emd(doc1, doc2):
    txt1 = open(doc1).read()
    txt2 = open(doc2).read()
    a = set(txt1.split())
    b = set(txt2.split())
    word2vec_model = gensim.models.KeyedVectors.load_word2vec_format('~/GoogleNews-vectors-negative300.bin', binary=True)
    word2vec_model.init_sims(replace=True)  # normalizes vectors
    mydistance = word2vec_model.wmdistance(a, b)
    return mydistance

def jaccard_similarity(doc1, doc2):
    txt1 = open(doc1).read()
    txt2 = open(doc2).read()
    a = set(txt1.split())
    b = set(txt2.split())
    similarity = float(len(a.intersection(b))*1.0/len(a.union(b))) #similarity belongs to [0,1] 1 means its exact replica.
    return similarity

@timed
def cossim(doc1, doc2):
    text_files = [doc1, doc2]
    documents = [open(f).read() for f in text_files]
    tfidf = TfidfVectorizer().fit_transform(documents)
    # no need to normalize, since Vectorizer will return normalized tf-idf
    pairwise_similarity = (tfidf * tfidf.T).A
    print (pairwise_similarity)
    return pairwise_similarity[0][1]

@timed
def diflib(doc1, doc2):
    txt1 = open(doc1).read()
    txt2 = open(doc2).read()
    x = difflib.SequenceMatcher(None, txt1, txt2).ratio()
    return x

@timed
def lev(doc1, doc2):
    txt1 = open(doc1).read()
    txt2 = open(doc2).read()
    p = distance.nlevenshtein(txt1.lower().strip(), txt2.lower().strip(), method=2)
    return p
def jac(doc1, doc2):
    s = distance.jaccard(doc1.lower().strip(), doc2.lower().strip())
    return s
def hamm(doc1, doc2):
    q = distance.hamming(doc1.lower().strip(), doc2.lower().strip())
    return q
def sorensen(doc1, doc2):
    z = distance.sorensen(doc1.lower().strip(), doc2.lower().strip())
    return z

def fastcmp(doc1, doc2):
    i = distance.fast_comp(doc1.lower().strip(), doc2.lower().strip())
    return i


def thedifflib():
    verbose = 0
    mypath = '~/test'
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    ## read all the txt files so as not to read it severally
    fileData = [' '.join(open(join(mypath, f), 'r').read().split()[1:]) for f in onlyfiles]
    ## intialize an empty dataframe
    new_df = pd.DataFrame()
    ## iterate between files and find the similarity metric
    i = 0
    for f1 in fileData:
        j = 0
        for f2 in fileData:
            if i == j:
                new_df.loc[i, j] = 1

            if verbose:  # and (j%100 == 0):
                print ('currently processing', onlyfiles[i], ' with ', onlyfiles[j])

            if i != j:
                new_df.loc[i, j] = difflib.SequenceMatcher(None, f1, f2).ratio()

            j += 1
        i += 1

    new_df.columns = onlyfiles
    new_df.index = onlyfiles
    print ('all calculations made. Exporting to mda_similarity_difflib_serial.csv')
    new_df.to_csv('mda_similarity_difflib_serial.csv', encoding='utf-8')
    print ('Export to csv done!')

def thelevenstein():
    verbose = 0
    mypath = '~/test'
    ## get the list of all files
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    ## read all the txt files so as not to read it severally
    fileData = [' '.join(open(join(mypath, f), 'r').read().split()[1:]) for f in onlyfiles]
    ## intialize an empty dataframe
    new_df = pd.DataFrame()
    ## iterate between files and find the similarity metric
    i = 0
    for f1 in fileData:
        # print 'currently processing ', onlyfiles[i]
        j = 0
        for f2 in fileData:
            if i <= j:
                new_df.loc[i, j] = distance.nlevenshtein(f1.lower().strip(), f2.lower().strip(), method=2)
            if verbose and (j % 100 == 0):
                print ('currently processing', onlyfiles[i], ' with ', onlyfiles[j])
            j += 1
        i += 1
    new_df.columns = onlyfiles
    new_df.index = onlyfiles
    print ('all calculations made. Exporting to csv')
    new_df.to_csv('document_similarity_levenstein_business.csv', encoding='utf-8')
    print ('Export to csv done!')
