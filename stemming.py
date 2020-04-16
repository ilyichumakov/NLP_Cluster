from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
import json
import os
import re

stemmer = SnowballStemmer("russian", True)

def retrieveCourseJSON(path):
    data = {}
    try:
        with open(path) as json_file:
            data = json.load(json_file)
    except:
        print("error opening " + path + " as JSON")

    return data

def token_and_stem(text):
    tokens = [word for sent in sent_tokenize(text) for word in word_tokenize(sent)]
    filtered_tokens = []
    for token in tokens:
        if re.search('[а-яА-Я]', token):
            filtered_tokens.append(token)
    #stems = [stemmer.stem(t) for t in filtered_tokens]
    res = ""
    for t in filtered_tokens:
        res = res + ' ' + stemmer.stem(t)
    #return stems
    return res

def token_only(text):
    tokens = [word.lower() for sent in sent_tokenize(text) for word in word_tokenize(sent)]
    filtered_tokens = []
    for token in tokens:
        if re.search('[а-яА-Я]', token):
            filtered_tokens.append(token)
    return filtered_tokens

def getCourseList(path):
    if not os.path.exists(path):
        raise ValueError("Path not found")
    files = os.scandir(path)
    result = []
    for entity in files:
        if re.fullmatch("(.*)\.json", entity.name):
            result.append(entity.path)
    return result

root = "D:/Третий курс/ФЛП/КР/степик"
targetRoot = os.path.join(root, "stemmed/")

courses = getCourseList(os.path.join(root, "allRelevant/"))
k = 0

for path in courses:
    course = retrieveCourseJSON(path)
    name = path.split("/").pop()
    stemmedCourse = {}
    for key in course.keys():
        if isinstance(course[key], str):
            stemmedCourse[key] = token_and_stem(course[key])
        elif isinstance(course[key], list):
            stemmedCourse[key] = []
            for item in course[key]:
                if isinstance(item, str):
                    stemmedCourse[key].append(token_and_stem(item))
        else:
            stemmedCourse[key] = course[key]

    with open(os.path.join(targetRoot, name), 'w') as outfile:
        json.dump(stemmedCourse, outfile)

    k = k + 1
    if k % 100 == 0:
        print(k, "обработано")

print("done")