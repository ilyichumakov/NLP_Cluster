from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import json
import os
import re
import pickle

def singleString(entity):
    res = ''
    if isinstance(entity, str):
        return entity

    elif isinstance(entity, list):
        for item in entity:
            res = res + singleString(item)
    
    return res

def retrieveCourseSingleString(path):
    data = {}
    try:
        with open(path) as json_file:
            data = json.load(json_file)
    except:
        print("error opening " + path + " as JSON")

    res = ''

    for item in data:
        if item != 'slug':
            res = res + singleString(data[item])

    return res

def getCourseList(path):
    if not os.path.exists(path):
        raise ValueError("Path not found")
    files = os.scandir(path)
    result = []
    for entity in files:
        if re.fullmatch("(.*)\.json", entity.name):
            result.append(entity.path)
    return result


def createMatrix(root, force = False):
    stop_words = stopwords.words('russian')
    stop_words.extend(['что', 'это', 'так', 'вот', 'быть', 'как', 'в', '—', '–', 'к', 'на', '...'])

    if os.path.exists(os.path.join(root, "tfidf.pickle")) and not force:
        tfidf_matrix = pickle.load(open(os.path.join(root, "tfidf.pickle"), "rb"))
    else:
        files = getCourseList(os.path.join(root, "stemmed/"))

        res = []

        for item in files:
            res.append(retrieveCourseSingleString(item))
        
        tfidf_vectorizer = TfidfVectorizer(
            max_df=0.5, 
            max_features=10000,
            min_df=0.005, stop_words=stop_words,
            use_idf=True, ngram_range=(2,2)
        )

        tfidf_matrix = tfidf_vectorizer.fit_transform(res)
        pickle.dump(tfidf_matrix, open(os.path.join(root, "tfidf.pickle"), "wb"))

    return(tfidf_matrix)

# example:
# createMatrix("D:/Третий курс/ФЛП/КР/степик")