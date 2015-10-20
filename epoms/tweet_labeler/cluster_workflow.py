execfile("cluster_helpers.py")

# Lines with %time comment could be run with %time prefix in ipython

num_clusters = 10
tweets = read_tweets()

stopwords = nltk.corpus.stopwords.words('english')
stemmer = SnowballStemmer("english")
stemmed_vocabulary, tokenized_vocabulary = build_vocabulary()  # %time 
vocab_df = pd.DataFrame({'words': tokenized_vocabulary}, index=stemmed_vocabulary)

tfidf_vectorizer = get_vectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(tweets)  # %time
terms = tfidf_vectorizer.get_feature_names()
distance = get_distance()  # %time 

km, clusters = get_clusters(num_clusters)
df = pd.DataFrame({'tweet': tweets, 'cluster': clusters}, index=[clusters], columns=['tweet', 'cluster'])

if False:
    print_clusters()

    print 'there are ' + str(vocab_df.shape[0]) + ' items in vocab_frame'
    print(tfidf_matrix.shape)
    print distance[0][0]
    print terms[:10]
    print(df['cluster'].value_counts())  # tweets per cluster
    print(df)
    if False:
        for t in tokenized_vocabulary[:1000]:
            print t