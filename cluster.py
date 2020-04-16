import numpy as np
import nltk
import os
from sklearn import feature_extraction
from sklearn.cluster import KMeans
from sklearn.cluster import MiniBatchKMeans
from sklearn.cluster import DBSCAN
from sklearn.cluster import AgglomerativeClustering
import pickle

root = "D:/Третий курс/ФЛП/КР/степик"

def clusterAndWrite(root, rewrite = False):
    if not os.path.exists(os.path.join(root, "tfidf.pickle")) or rewrite:
        print("Матрица весов не определена в файле :(\nНаучите меня получать её другим образом либо замаринуйте с именем tfidf.pickle")
        exit(0)

    tfidf_matrix = pickle.load(open(os.path.join(root, "tfidf.pickle"), "rb"))

    if not os.path.exists(os.path.join(root, "kMeans.pickle")) or rewrite:
        # K ближайших соседей
        km = KMeans(n_clusters=10)
        km.fit(tfidf_matrix)
        clusters = km.labels_.tolist()

        pickle.dump(km, open(os.path.join(root, "kMeans.pickle"), "wb"))

    if not os.path.exists(os.path.join(root, "MiniBatchKMeans.pickle")) or rewrite:
        # MiniBatchKMeans
        mbk = MiniBatchKMeans(init='random', n_clusters=10) #(init='k-means++', ‘random’ or an ndarray)
        mbk.fit_transform(tfidf_matrix)
        mbk.fit(tfidf_matrix)
        miniclusters = mbk.labels_.tolist()

        pickle.dump(mbk, open(os.path.join(root, "MiniBatchKMeans.pickle"), "wb"))

    if not os.path.exists(os.path.join(root, "DBSCAN.pickle")) or rewrite:
        # DBSCAN
        db = DBSCAN(eps=0.3, min_samples=10).fit(tfidf_matrix)
        labels = db.labels_

        pickle.dump(db, open(os.path.join(root, "DBSCAN.pickle"), "wb"))

    if not os.path.exists(os.path.join(root, "AgglomerativeClustering.pickle")) or rewrite:
        # Аггломеративная класстеризация
        agglo1 = AgglomerativeClustering(n_clusters=10, affinity='euclidean') #affinity можно выбрать любое или попробовать все по очереди: cosine, l1, l2, manhattan
        answer = agglo1.fit_predict(tfidf_matrix.toarray())
        pickle.dump(answer, open(os.path.join(root, "AgglomerativeClustering.pickle"), "wb"))

clusterAndWrite(root)