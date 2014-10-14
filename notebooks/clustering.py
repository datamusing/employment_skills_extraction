from sklearn.cluster import KMeans
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.feature_extraction import text 
import nltk.stem
global english_stemmer 
english_stemmer = nltk.stem.SnowballStemmer('english')
from collections import defaultdict
import collections, re, operator
from collections import Counter

class StemmedCountVectorizer(CountVectorizer):
    
    def build_analyzer(self):
        analyzer = super(CountVectorizer, self).build_analyzer()
        return lambda doc: (english_stemmer.stem(w) for w in analyzer(doc))



def Clustering(df,num_clusters,stop_words):
                 
    stop_words = text.ENGLISH_STOP_WORDS.union(stop_words)
    vectorizer = StemmedCountVectorizer(min_df=10, max_df=0.3,stop_words = stop_words)
    vectorized = vectorizer.fit_transform(df.feature)
    
    km = KMeans(n_clusters = num_clusters, init = 'k-means++', n_init = 1,verbose=1)
    clustered = km.fit(vectorized)
    predict = km.predict(vectorized)
    return predict


def get_features(gg,predict):
#This function returns a dictionary with cluster type & list of features. this list goes into bag of words to get word count
#gg: skills df grouped by cluster
#predict is the cluster number
    d=defaultdict()
    key=set(predict)
    for k in key:
        d[k]=[]
    for x,y in gg:
        d[x]+=list(y.feature.values)
    return d


def BagofWords(textlist,stop_words):
#returns bag of words for a list of texts
    stop_words = text.ENGLISH_STOP_WORDS.union(stop_words)
    bagsofwords = [collections.Counter(re.findall(r'\w+', txt))
            for txt in textlist]
    words=Counter()
    for bbb in bagsofwords:
        for bb,v in bbb.iteritems():
            if bb not in stop_words:
                words[bb]+=v
    sorted_words = sorted(words.iteritems(), key=operator.itemgetter(1),reverse=True)
    return sorted_words
