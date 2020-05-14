from ir import *
import os
import pickle

def sayGoodByeToYourComputer(root, rootTarget):
    #print("download started, it will take 19 hours in order to process it")
    #print(stepik.loadAllCourses(os.path.join(root, rootTarget), True))
    #print(stemming.stem(root, rootTarget, True))

    matrix = tfidf.createMatrix(root, False)
    print(cluster.clusterAndWrite(root, matrix, 5, False))

    files = tfidf.getCourseList(os.path.join(root, rootTarget))

    res = []

    for item in files:
        res.append(stemming.retrieveCourseJSON(item)["title"])
    
    kmeans = pickle.load(open(os.path.join(root, "kMeans.pickle"), "rb"))
    # minikmeans = pickle.load(open(os.path.join(root, "MiniBatchKMeans.pickle"), "rb"))
    # DBSCAN = pickle.load(open(os.path.join(root, "DBSCAN.pickle"), "rb"))
    # Agglomerative = pickle.load(open(os.path.join(root, "AgglomerativeClustering.pickle"), "rb"))

    visual.ipca2d(matrix, kmeans.labels_.tolist(), res, "К ближайших соседей")
    # visual.ipca2d(matrix, minikmeans.labels_.tolist(), res, "Компромиссный метод К ближайших соседей")
    # visual.ipca2d(matrix, DBSCAN.labels_, res, "DBSCAN")
    # visual.ipca2d(matrix, Agglomerative.tolist(), res, "Аггломеративная кластеризация")

# example:
sayGoodByeToYourComputer("D:/Третий курс/ФЛП/КР/степик", "allRelevant/")
# or you can use availiable methods partially if some steps (what a worldplay :D) are already done