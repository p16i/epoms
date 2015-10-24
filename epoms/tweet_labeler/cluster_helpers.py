import numpy as np
import pandas as pd
import nltk
import re
import os
import codecs
from sklearn import feature_extraction
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import matplotlib as mpl
from sklearn.manifold import MDS
import csv


def read_tweets(path):
    print "Reading tweets"
    with open(path, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        tweets = [row[3].decode('utf8') for row in spamreader if (len(row) > 1)]
    return tweets


def preprocess(tweet):
    # replace URLs with URL
    #         twitter images with TWITTERPIC
    tweet = re.sub(r'((mailto\:|(news|(ht|f)tp(s?))\://){1}\S+)', 'URL', tweet, flags=re.MULTILINE)
    tweet = re.sub(r'pic.twitter.com[^\s]*', 'TWITTERPIC', tweet, flags=re.MULTILINE)
    return tweet


def tokenize(text):
    tokens = [word for sentence in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sentence)]
    tokens = [t for t in tokens if re.search('[a-zA-Z]', t)]  # reject tokens that don't contain letters
    return tokens


def stem(tokens):
    return [stemmer.stem(t) for t in tokens]


def tokenize_and_stem(text):
    return stem(tokenize(text))


def build_vocabulary():
    print "\nBuilding vocabulary"
    stemmed_vocabulary, tokenized_vocabulary = [], []
    for t in tweets:
        tweet = preprocess(t)
        stemmed_vocabulary.extend(tokenize_and_stem(tweet))
        tokenized_vocabulary.extend(tokenize(tweet))
    return stemmed_vocabulary, tokenized_vocabulary


def get_vectorizer():
    print "\nGetting vectorizer"
    return(TfidfVectorizer(max_df=0.8, max_features=150000,
                           min_df=0.01, stop_words='english',
                           use_idf=True, tokenizer=tokenize_and_stem, ngram_range=(1, 1)))


def get_distance():
    print "\nGetting distance"
    return(1 - cosine_similarity(tfidf_matrix))


def get_clusters(num_clusters):
    print "\nGetting clusters"
    km = KMeans(n_clusters=num_clusters)
    km.fit(tfidf_matrix)
    return km, km.labels_.tolist()


def print_clusters():
    print("\nTop terms per cluster:\n")
    cluster_ordered_terms = km.cluster_centers_.argsort()[:, ::-1]  # sort words in cluster by proximity to centroid

    for i in range(num_clusters):
        print("Cluster %d words:" % i)

        for term_i in cluster_ordered_terms[i, :6]:
            top_term = vocab_df.ix[terms[term_i].split(' ')].values.tolist()[0][0]
            top_term = str(top_term).encode('utf-8', 'ignore')
            print(' %s' % top_term)
        print "\n\n"

        print("Cluster %d tweets:" % i)
        for o in df.ix[i]['tweet'].values.tolist()[:10]:
            print(o)
        print "\n\n"

