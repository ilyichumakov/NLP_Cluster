from ir import *
import os

def sayGoodByeToYourComputer(root, rootTarget):
    #print("download started, it will take 19 hours in order to process it")
    #print(stepik.loadAllCourses(os.path.join(root, rootTarget), True))
    print(stemming.stem(root, rootTarget, True))

    matrix = tfidf.createMatrix(root)
    print(cluster.clusterAndWrite(root, matrix))

# example:
# sayGoodByeToYourComputer("D:/Третий курс/ФЛП/КР/степик", "allRelevant/")
# or you can use availiable methods partially if some steps (what a worldplay :D) are already done