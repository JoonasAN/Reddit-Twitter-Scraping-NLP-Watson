"""This module has work-in-progress functions for NLP pre-prosessing and Vectorization"""
import re
import pandas as pd
import cmas
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import string


# Pre-

def remove_newlines(data):
    # remove exess newlines
    data = data['text'].replace(['\\r','\\n\\n', '\\n'],['','\\n', ' '], regex=True)

    return data

def tokenize(data):
    # remove punct
    data['text_nopunct'] = data['text'].apply(lambda x: cmas.remove_punct(x.lower()))
    # We convert to lower as Python is case-sensitive.
    data['text_tokenized'] = data['text_nopunct'].apply(lambda x: re.split('\W+', x.lower())) # W+ means that either a word character (A-Za-z0-9_) or a dash (-) can go there. 
    
    print(data)
    return data

def remove_stopwords(data):

    stopword = nltk.corpus.stopwords.words('english') # All English Stopwords
    # remove stopwords
    data['text_nostop'] = data['text_tokenized'].apply(lambda x: [word for word in x if word not in stopword])
    print(data)
    return data

def stemming(data):
    ps = nltk.PorterStemmer()
    data['text_stemmed'] = data['text_nostop'].apply(lambda x: [ps.stem(word) for word in x])
    return data

def lemmatizing(data):
    wn = nltk.WordNetLemmatizer()
    data['text_lemmatized'] = data['text_nostop'].apply(lambda x: [wn.lemmatize(word) for word in x])
    return data

def clean_text(text):
    ps = nltk.PorterStemmer()
    stopwords = nltk.corpus.stopwords.words('english')

    text = "".join([word.lower() for word in text if word not in string.punctuation])
    tokens = re.split('\W+', text)
    text = [ps.stem(word) for word in tokens if word not in stopwords]
    return text

def count_punct(text):
        count = sum([1 for char in text if char in string.punctuation])
        return round(count/(len(text) - text.count(" ")), 3)*100

def count_lenght_text(data):
    # Function to calculate length of text excluding space

    data['len'] = data['text'].apply(lambda x: len(x) - x.count(" "))
    data['punct%'] = data['text'].apply(lambda x: count_punct(x))

    return (data)


# --------------- From this point on I have no clue how well functions work ---------------------------
# Vectorizing functions


def bag_of_words(data):
    count_vect = CountVectorizer(analyzer=clean_text)
    X_counts = count_vect.fit_transform(data['text'])
    #print(X_counts.shape)
    #print(count_vect.get_feature_names())
    X_counts_df = pd.DataFrame(X_counts.toarray(), columns=count_vect.get_feature_names())
    X_counts_df.head(10)

def n_grams(data):
    ngram_vect = CountVectorizer(ngram_range=(2,2),analyzer=clean_text) # It applies only bigram vectorizer
    X_counts = ngram_vect.fit_transform(data['text'])
    #print(X_counts.shape)
    #print(ngram_vect.get_feature_names())
    X_counts_df = pd.DataFrame(X_counts.toarray(), columns=ngram_vect.get_feature_names())
    X_counts_df.head(10)

def tf_idf(data):
    tfidf_vect = TfidfVectorizer(analyzer=clean_text)
    X_tfidf = tfidf_vect.fit_transform(data['text'])
    #print(X_tfidf.shape)
    #print(tfidf_vect.get_feature_names())
    X_tfidf_df = pd.DataFrame(X_tfidf.toarray(), columns=tfidf_vect.get_feature_names())
    X_tfidf_df.head(10)




if __name__=="__main__":
    data = pd.read_csv("./data/data_tone.csv")
    data = tokenize(data)
