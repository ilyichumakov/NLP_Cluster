import requests
import os
import re
import json

def getCourseList():
    request = requests.get("https://stepik.org:443/api/course-lists")
    body = request.json()
    clist = []
    for i in body["course-lists"]:
        clist.append({"title": i["title"], "courses": i["courses"] })        

    return clist

def getUser(id):
    request = requests.get("https://stepik.org:443/api/users/" + str(id))
    body = request.json()["users"][0]
    return body

def retrieveUserValuableInfo(user):
    useful = [
        "details",
        "first_name",
        "last_name",
        "short_bio",
        "city"
    ]

    res = {}

    for key in useful:
        res[key] = user[key]

    return res

def getCourseInfo(courseId):
    request = requests.get("https://stepik.org:443/api/courses/" + str(courseId))
    body = request.json()["courses"][0]
    return body

def getNextPage(page):
    request = requests.get("https://stepik.org:443/api/courses?language=ru&page=" + str(page))
    courses = request.json()["courses"]
    return {'meta': request.json()["meta"], 'courses': courses}

def getSection(id):
    request = requests.get("https://stepik.org:443/api/sections/" + str(id))
    body = request.json()["sections"]
    return body

def getUnit(id):
    request = requests.get("https://stepik.org:443/api/units/" + str(id))
    body = request.json()["units"]
    return body

def getLesson(id):
    request = requests.get("https://stepik.org:443/api/lessons/" + str(id))
    body = request.json()["lessons"]
    return body

def retrieveTitles(sections):
    titles = []
    for sectionId in sections:
        section = getSection(sectionId)[0]
        titles.append(section["title"])
        if "units" in section:
            for unitId in section["units"]:
                unit = getUnit(unitId)[0]                        
                if "lesson" in unit:
                    lesson = getLesson(unit["lesson"])[0]
                    titles.append(lesson["title"])

    return titles

def writeCourseToFile(target, course):
    if course["learners_count"] < 50:
        return True
    name = re.sub("[\?\\/!:\*<>\|\"]", "_", course["title"])
    cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    course["summary"] = re.sub(cleanr, '', course["summary"])
    course["target_audience"] = re.sub(cleanr, '', course["target_audience"])
    course["title"] = re.sub(cleanr, '', course["title"])
    course["description"] = re.sub(cleanr, '', course["description"])

    needFileds = [
        "id",
        "summary",
        "target_audience",
        "requirements",
        "description",
        "sections",
        "authors",
        "learners_count",
        "is_popular",
        "title",
        "slug"
    ]

    try:
        
        info = {}
        for key in needFileds:
            info[key] = course[key]

        users = []

        titles = retrieveTitles(info["sections"])

        info["titles"] = titles

        if "authors" in info:
            for userId in info["authors"]:
                users.append(retrieveUserValuableInfo(getUser(userId)))

            info["authors"] = users

        with open(os.path.join(target, name + ".json"), 'w') as outfile:
            json.dump(info, outfile)

    except:
        print(name + " occured an error, skipped\n")

    return True

def loadCoursesByGroups(targetPath):
    sections = getCourseList()
    for sect in sections:
        currentPath = os.path.join(targetPath, sect["title"])
        if not os.path.exists(currentPath):
            os.mkdir(currentPath)
        for course in sect["courses"]:        
            info = getCourseInfo(course)
            if info["learners_count"] < 50:
                continue
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

def loadAllCourses(targetPath, debug = False):
    k = 0
    page = getNextPage(1)
    while(page["meta"]["has_next"]):
        for course in page["courses"]:
            if writeCourseToFile(targetPath, course):
                k += 1
                if debug and k % 50 == 0:
                    print("Записано", k, "курсов")
            
        page = getNextPage(page["meta"]["page"] + 1)

    return "download finished"

# example:
# loadAllCourses("D:/Третий курс/ФЛП/КР/степик/allRelevant/")