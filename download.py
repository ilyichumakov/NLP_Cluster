import requests
import os
import re


def getCourseList():
    request = requests.get("https://stepik.org:443/api/course-lists")
    body = request.json()
    clist = []
    for i in body["course-lists"]:
        clist.append({"title": i["title"], "courses": i["courses"] })        

    return clist

def getCourseInfo(courseId):
    request = requests.get("https://stepik.org:443/api/courses/" + str(courseId))
    body = request.json()["courses"][0]
    return {'title': body["title"], 'target_audience': body["target_audience"], 'authors': body["authors"], 'description': body["description"]}

def getNextPage(page):
    request = requests.get("https://stepik.org:443/api/courses?page=" + str(page))
    courses = request.json()["courses"]
    return {'meta': request.json()["meta"], 'courses': courses}

def writeCourseToFile(target, course):
    name = re.sub("[\?\\/!:\*<>\|\"]", "_", course["title"])
    f = open(os.path.join(target, name + ".txt"), "w", encoding="utf-8")
    f.write(course["title"] + "\n")
    f.write(course["target_audience"] + "\n")
    cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    cleanDescription = re.sub(cleanr, '', course["description"])
    #f.write(course["description"] + "\n")
    f.write(cleanDescription + "\n")
    f.close()
    return True

def loadCoursesByGroups(targetPath):
    sections = getCourseList()
    for sect in sections:
        currentPath = os.path.join(targetPath, sect["title"])
        if not os.path.exists(currentPath):
            os.mkdir(currentPath)
        for course in sect["courses"]:        
            info = getCourseInfo(course)
            f = open(os.path.join(currentPath, info["title"] + ".txt"), "w", encoding="utf-8")
            f.write(info["title"] + "\n")
            f.write(info["target_audience"] + "\n")
            #f.write(info["authors"] + "\n") # here we have id's of authors, so need to get them separately
            cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
            cleanDescription = re.sub(cleanr, '', info["description"])
            #f.write(info["description"] + "\n")
            f.write(cleanDescription + "\n")
            f.close()

    return "done"

def loadAllCourses(targetPath):

    page = getNextPage(1)
    while(page["meta"]["has_next"]):
        for course in page["courses"]:
            writeCourseToFile(targetPath, course)
        page = getNextPage(page["meta"]["page"] + 1)

    return "done"

#print(loadCoursesByGroups("D:/Третий курс/ФЛП/КР/степик/"))
print(loadAllCourses("D:/Третий курс/ФЛП/КР/степик/all/"))