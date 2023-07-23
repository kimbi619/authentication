import re
from .subjects import subjects
import json

import os


def extractData():
    data = []
    file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'file.txt')
    with open(file, "r") as txt_file:
        lines = txt_file.readlines()
        for i in range(0, len(lines)):
            line = lines[i]
            list = re.sub(r'\d+|[()]', '', line)
            studentList = list.replace('Advonced Level Results', '').replace(
                'RESULTS OF SUCCESSFUL CANDIDATES', '').replace('Cameroon GCE Board', '').replace("'", '')

            parts = studentList.split(',')
            if parts.__len__() < 2:
                continue

            namepart = parts[0].rsplit('-', 2)
            name = namepart[0].strip()

            subjectTitle = subjectMapping(namepart[1].strip())
            grade = namepart[2]

            grades = [{"title":subjectTitle, "grade": grade}]

            for s in parts[1: -1]:
                subjectTitle, grade = s.split('-', 1)
                subject = {"title": subjectMapping(subjectTitle.strip()),
                           "grade": grade.strip()}
                grades.append(subject)

            student = {
                "name": name,
                "grades": grades
            }
            data.append(student)
        return data

def subjectMapping(code):
    for subject in subjects:
        if subject['code'] == code:
            return subject['title']
    return code


def fetchAllData():
    return extractData()





def preProcessed():

    file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ALG_2019.txt')
    results = []
    data=''
    with open(file, "r") as txt_file:
        data = txt_file.read()
        
    # print(data)
    data = json.loads(data)

    for item in data:
        name = item['student_name']
        all_grades = item['student_grades']
        
        grades = []
        gradeList = all_grades.split(',')

        for gradeItem in gradeList:
            if len(gradeItem) == 4:
                subjectTitle = gradeItem[:3]
                grade = gradeItem[-1]
            else:
                subjectTitle, grade = gradeItem.split('-', 1)

            subject = {"title": subjectMapping(subjectTitle.strip()),
                        "grade": grade.strip()}
            grades.append(subject)
        student = {
            "name": name,
            "grades": grades
        }
        results.append(student)
    return results

