import re

def extractData():
    data = []
    with open("file.txt", "r") as txt_file:
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

            subjectTitle = namepart[1]
            grade = namepart[2]

            grades = [{"title": subjectTitle, "grade": grade}]

            for s in parts[1: -1]:
                subjectTitle, grade = s.split('-', 1)
                subject = {"title": subjectTitle.strip(),
                           "grade": grade.strip()}
                grades.append(subject)

            student = {
                "name": name,
                "grades": grades
            }
            data.append(student)
        return data


# def saveData(data):
#     print(response)

def fetchAllData():
    return extractData()


