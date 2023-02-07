from canvasapi import Canvas
import os
import requests
import helper
import shutil
from os import listdir
from os.path import join, isfile
import threading
from zipfile import ZipFile

def threadedfunc(student, sub):
    # print(student.name)
    rubric = sub.rubric_assessment if hasattr(sub, 'rubric_assessment') else helper.rubric_blank_60_Final()
    if hasattr(sub, 'attachments'):
        attachment = sub.attachments[0]
        # print(attachment['filename'])
        response = requests.get(attachment['url'])
        os.mkdir(student.name)
        open(student.name + "/" + attachment['filename'], "wb").write(response.content)  # Download file
        with ZipFile(student.name + "/" + attachment['filename'], 'r') as zipObj:
            zipObj.extractall(student.name)
        try:
            onlyfiles = [f for f in listdir(student.name) if isfile(join(student.name, f))]
            fname = onlyfiles[0]
            for file in onlyfiles:
                if '.c' in file:
                    with open(student.name + '/' + file) as hand:
                        text = hand.read()
                        if 'main' in text:
                            fname = file
                            break

            with open(student.name + "/" + fname, errors='ignore') as file:
                data = file.read().lower()
        except Exception as e:
            print(str(e))
            for key, value in rubric.items(): value['comments'] = 'File Read Error.'
        else:
            rubric = helper.rubric_1(rubric, '_4123', data)

            rubric = helper.rubric_2(rubric, '_6418', data)

            rubric = helper.rubric_auto_3_4_5(rubric, '_9510', '_2366', '_6591','',[["1	1.0000	1.0000	1.0000\n4	2.0000	1.5874	1.4142\n5	2.2361	1.7100	1.4953\n6	2.4495	1.8171	1.5651"],["1	1.0000	1.0000	1.0000"],["4	2.0000	1.5874	1.4142"],["5	2.2361	1.7100	1.4953"],["6	2.4495	1.8171	1.5651"]], student.name + "/" + attachment['filename'])

    else:
        for key, value in rubric.items(): value['comments'] = 'No Submission.'
        helper.print_rubric(rubric)

    print('\n')
    print(student.name)
    helper.print_rubric(rubric)
    # sub.edit(**{'rubric_assessment':rubric})


API_URL = "https://canvas.instructure.com/"
API_KEY = "" # Canvas API Key

PATH = "" # Path to project

canvas = Canvas(API_URL, API_KEY) # Initialize a new Canvas object
tacourse = canvas.get_courses(enrollment_type='ta')[0] #Get Course

assignment_name = 'Final Project' # name of assignmnet to grade

assignments = tacourse.get_assignments()
assignment = [assignment for assignment in assignments if assignment_name in assignment.name][0]
students = tacourse.get_users(enrollment_type=['student'])
for student in students:
    sub = assignment.get_submission(student.id,include='rubric_assessment')
    if sub.grade and not student.name in [""]:
        continue
    # threadedfunc(student,sub)
    t=threading.Thread(target=threadedfunc, args=(student,sub,))
    t.start()