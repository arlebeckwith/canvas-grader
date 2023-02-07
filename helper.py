import subprocess
import requests
from os import listdir
from os.path import join, isfile
import shutil

def rubric_3_4_5(rubric, id1, id2, id3, filename):
    tmp = subprocess.run(["gcc", filename], stderr=subprocess.PIPE)  # grade compile with no errors
    if tmp.returncode == 1:
        rubric[id3]['comments'] = 'Program did not compile.'
    else:
        rubric[id3]['points'] = 5
        rubric[id3]['comments'] = 'Compiled Correctly.'
        rubric[id2]['points'] = int(input("Run Grade:"))
        rubric[id1]['points'] = int(input("Correct Output Grade:"))
        rubric[id2]['comments'] = "Runs without Crashing." if rubric[id2]['points'] == 5 else 'Doesnt Run.'
        rubric[id1]['comments'] = "Correct output." if rubric[id1]['points'] == 10 else 'Incorrect Output.'
    return rubric

def program6(output):
    sp = output.split('\r')
    arr = []
    for i, o in enumerate(sp):
        o.strip()
        arr.append([sub for sub in o if sub != ' ' and sub != '\n'])
        if not arr[-1]:
            arr.pop()

    alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    abnum = 0
    x, y = 0, 0
    if arr[x][y] == 'a':
        arr[x][y] = '.'
        while True:
            abnum = abnum + 1
            if x > 0:
                if arr[x-1][y] == alphabet[abnum % 26]:
                    x = x - 1
                    arr[x][y] = '.'
                    continue

            if x < len(arr) - 1:
                if arr[x+1][y] == alphabet[abnum % 26]:
                    x = x + 1
                    arr[x][y] = '.'
                    continue

            if y > 0:
                if arr[x][y-1] == alphabet[abnum % 26]:
                    y = y - 1
                    arr[x][y] = '.'
                    continue

            if y < len(arr[0]) - 1:
                if arr[x][y+1] == alphabet[abnum % 26]:
                    y = y + 1
                    arr[x][y] = '.'
                    continue

            break;

    else:
        return False

    return all(p == ['.','.','.','.','.','.','.','.','.','.'] for p in arr)

def rubric_auto_3_4_5(rubric, id1, id2, id3, input_c, expected, filename):
    dirdel = True
    tmp = subprocess.run(["make", '-s','-C',filename.split('/')[0]], stderr=subprocess.PIPE)  # grade compile with no errors
    # tmp = subprocess.run(["gcc", filename ,'-o', filename.split('/')[0] + '/a.exe'], stderr=subprocess.PIPE)  # grade compile with no errors

    if tmp.returncode == 1:
        rubric[id3]['comments'] = "Didn't Compile." #tmp.stderr.decode()
    else:
        rubric[id3]['points'] = 10
        rubric[id3]['comments'] = 'Compiled Correctly.'
        onlyfiles = [f for f in listdir(filename.split('/')[0]) if isfile(join(filename.split('/')[0], f))]
        execute = None
        for file in onlyfiles:
            if 'exe' in file:
                execute = file
                break
        if execute:
            out = subprocess.Popen([filename.split('/')[0] + "/" + execute, 'input.txt', filename.split('/')[0] + "/" + "output.txt"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # out.stdin.write(input_c.encode('utf-8'))
            out.stdin.flush()
            try:
                out.wait(timeout=10)
            except subprocess.TimeoutExpired:
                out.kill()
                # dirdel = False
            if not out.stderr.read():
                rubric[id2]['points'] = 10
                rubric[id2]['comments'] = 'Runs without Crashing.'
                output = out.stdout.read().decode().lower()

                with open(filename.split('/')[0] + "/output.txt") as file:
                    output = file.read()

                correctArray = [all(ex.lower() in output for ex in expect) for expect in expected]
                rubric[id1]['points'] = round(20*sum(correctArray)/len(correctArray))
                if rubric[id1]['points'] == 20:
                    rubric[id1]['comments'] = 'Correct output.'
                else:
                    # rubric[id1]['comments'] = output
                    rubric[id1]['comments'] = '\n'.join(["Input: " + input_c.strip(),"Expected: " + ', '.join(expected[0]),"Received: " + ' '.join([e.strip() for e in output.split('\n') if e])])
                # else:
                #     rubric[id1]['points'] = int(input("Correct Output Grade:"))
            # else:
                # rubric[id2]['points'] = int(input("Run Grade:"))
                # rubric[id1]['points'] = int(input("Correctness Points:"))
            else:
                rubric[id2]['comments'] = 'Did not run Properly.' #out.stderr.read()
        else:
            # dirdel = False
            rubric[id3]['comments'] = "Makefile didn't create .exe."
            rubric[id3]['points'] = 0

    # print(rubric[id3]['points'], [rubric[id3]['comments']])
    # print(rubric[id2]['points'], [rubric[id2]['comments']])
    # print(rubric[id1]['points'], [rubric[id1]['comments']])
    if dirdel:
        # shutil.rmtree(filename.split('/')[0])
        pass
    return rubric

def rubric_1(rubric, id, data):
    grade = 0
    comments = []
    if 'unction' in data:  # grade header and pseudocode
        grade = grade + 2
    else:
        comments.append('Missing Function Heading.')
    if 'ummary' in data:
        grade = grade + 2
    else:
        comments.append('Missing Summary Heading.')
    if 'nputs' in data:
        grade = grade + 2
    else:
        comments.append('Missing Inputs Heading.')
    if 'utputs' in data:
        grade = grade + 2
    else:
        comments.append('Missing Outputs Heading.')
    if 'seudocode' in data:
        grade = grade + 2
    else:
        comments.append('Missing Pseudocode Heading.')
    if grade == 10: comments = ["Great Job!"]
    rubric[id]['points'] = grade
    rubric[id]['comments'] = '\n'.join(comments)
    # print(rubric[id]['points'], [rubric[id]['comments']])
    return rubric

def rubric_2(rubric, id, data):
    # print(rubric[id]['points'])
    if 'pseudocode' in data:
        if 'end' in data:
            pseudo = data.split("end", 1)[0]
            if 'begin' in pseudo:
                pseudo = pseudo.split("begin", 1)[1].split('\n')  # grade comment, pseudocode match
                pseudo = [i[1:].strip() for i in pseudo if i[1:].strip()]
                fileEnd = data.split('end', 1)[1]
                matches = 0
                for p in pseudo:
                    if p in fileEnd:
                        matches = matches + 1
                if len(pseudo):
                    rubric[id]['points'] = round((matches / len(pseudo)) * 10)
                rubric[id]['comments'] = "{} lines in pseudocode, {} match.".format(len(pseudo), matches)
            else:
                rubric[id]['comments'] = 'Missing Begin in pseudocode.'
        else:
            rubric[id]['comments'] = 'Missing End in pseudocode.'
    else:
        rubric[id]['comments'] = 'No Pseudocode header.'
    # print(rubric[id]['points'], [rubric[id]['comments']])
    return rubric

def rubric_1_pseduo_check(rubric, id, data):
    if rubric[id]['points'] == 5:
        print('Already 5')
    else:
        print(data.split('*/')[0])
        rubric[id]['points'] = input('Grade:{}->'.format(rubric[id]['points']))
    return rubric

def rubric_blank_30():
    return {'_9847': {'rating_id': 'blank', 'comments': '', 'points': 0},
            '_8385': {'rating_id': '_7017', 'comments': '', 'points': 0},
            '_8185': {'rating_id': '_1588', 'comments': '', 'points': 0},
            '_2785': {'rating_id': '_3889', 'comments': '', 'points': 0},
            '_252': {'rating_id': '_2244', 'comments': '', 'points': 0}}

def rubric_blank_60_Final():
    return {'_4123': {'rating_id': 'blank', 'comments': '', 'points': 0},
            '_6418': {'rating_id': '_7017', 'comments': '', 'points': 0},
            '_6591': {'rating_id': '_1588', 'comments': '', 'points': 0},
            '_2366': {'rating_id': '_3889', 'comments': '', 'points': 0},
            '_9510': {'rating_id': '_2244', 'comments': '', 'points': 0}}

def rubric_blank_60():
    return {'_9847': {'rating_id': 'blank', 'comments': '', 'points': 0},
            '_8385': {'rating_id': '_7017', 'comments': '', 'points': 0},
            '_8185': {'rating_id': '_1588', 'comments': '', 'points': 0},
            '_2785': {'rating_id': '_3889', 'comments': '', 'points': 0},
            '_252': {'rating_id': '_2244', 'comments': '', 'points': 0},
            '166403_5070': {'rating_id': '166403_3280', 'comments': '', 'points': 0},
            '166403_9243': {'rating_id': '166403_1726', 'comments': '', 'points': 0},
            '166403_5714': {'rating_id': '166403_5919', 'comments': '', 'points': 0},
            '166403_7184': {'rating_id': '166403_3442', 'comments': '', 'points': 0},
            '166403_2517': {'rating_id': '166403_874', 'comments': '', 'points': 0}}


def print_rubric(rubric):
    for key, value in rubric.items(): print(value['points'], [value['comments']])

def grade_lower_file(attachment, rubric, inputed, expected):
    response = requests.get(attachment['url'])
    open(attachment['filename'], "wb").write(response.content)  # Download file
    try:
        with open(attachment['filename']) as file:
            data = file.read().lower()
    except:
        for key, value in rubric.items(): value['comments'] = 'File Read Error.'
    else:
        rubric = rubric_1(rubric, '_9847', data)

        rubric = rubric_2(rubric, '_8385', data)

        rubric = rubric_3_4_5(rubric, '_252', '_2785', '_8185', attachment['filename'])

        # os.remove(attachment['filename'])
    return rubric

def grade_upper_file(attachment, rubric, inputed, expected):
    response = requests.get(attachment['url'])
    open(attachment['filename'], "wb").write(response.content)  # Download file
    try:
        with open(attachment['filename']) as file:
            data = file.read().lower()
    except:
        for key, value in rubric.items(): value['comments'] = 'File Read Error.'
    else:
        rubric = rubric_1(rubric, '166403_5070', data)

        rubric = rubric_2(rubric, '166403_9243', data)

        rubric = rubric_3_4_5(rubric, '166403_2517', '166403_7184', '166403_5714', attachment['filename'])

        # os.remove(attachment['filename'])
    return rubric


