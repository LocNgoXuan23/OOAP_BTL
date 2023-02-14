from turtle import update
from venv import create
from model import *
from utils import *
import re
from PyQt5.QtWidgets import QMessageBox

def check_username_exist(username):
    mycursor.reset()
    mycursor.execute(f'SELECT * FROM Users WHERE username=\'{username}\'')
    user = mycursor.fetchone()
    if user == None:
        return 1
    else:
        return -1

def create_account(username, passwd, role):
    status = check_username_exist(username)

    if status == -1:
        return -1
    else:
        date_time = datetime.now()
        mycursor.execute("INSERT INTO Users (username, passwd, created, role) VALUES (%s,%s,%s,%s)", (username, passwd, date_time, role))
        last_id = mycursor.lastrowid
        flag = 0
    while True:
        msg_box = QMessageBox()
        msg_box.setFixedSize(400, 300)
        if (len(passwd)<=8):
            flag = -1
            break
        elif not re.search("[a-z]", passwd):
            flag = -1
            break
        elif not re.search("[A-Z]", passwd):
            flag = -1
            break
        elif not re.search("[0-9]", passwd):
            flag = -1
            break
        elif not re.search("[_@$]" , passwd):
            flag = -1
            break
        elif re.search("\s" , passwd):
            flag = -1
            break
        else:
            flag = 0
            break
        
    if flag == -1:
        create_account(username, passwd, role)
        msg_box.setText("Password Not Validate !!")
        msg_box.exec_()
    elif flag == 0:
        if role == '1':
            mycursor.execute("INSERT INTO Managers (id, created) VALUES (%s,%s)", (last_id, date_time))
        elif role == '2':
            mycursor.execute("INSERT INTO Teachers (id, created) VALUES (%s,%s)", (last_id, date_time))
        elif role == '3':
            mycursor.execute("INSERT INTO Students (id, created) VALUES (%s,%s)", (last_id, date_time))
        db.commit()

        return 1

def create_class(className, teacherId):
    # return
    # 1: success
    # -1: exist teacher_id in one avalable class

    if teacherId != -1:
        class_id = get_class_id_by_teacher_id_from_class(teacherId)
        if class_id != -1:
            return -1
        else:
            date_time = datetime.now()
            mycursor.reset()
            mycursor.execute("INSERT INTO Classes (created, className, teacherId) VALUES (%s,%s,%s)", (date_time, className, teacherId))
            db.commit()
            return 1

def create_subject_class(subjectName, teacherId):
    date_time = datetime.now()
    mycursor.reset()
    mycursor.execute("INSERT INTO SubjectClasses (created, subjectName, teacherId) VALUES (%s,%s,%s)", (date_time, subjectName, teacherId))
    db.commit()

    mycursor.reset()
    mycursor.execute(f'SELECT id FROM SubjectClasses WHERE teacherId={teacherId}')
    subject_class_item = mycursor.fetchall()

    return subject_class_item[-1][0]

def show_table(table_name):
    mycursor.reset()

    Q = f'SELECT * FROM {table_name}'
    mycursor.execute(Q)
    for x in mycursor:
        print(x)

def remove_item(table_name, id_key, id):
    Q = f'DELETE FROM {table_name} WHERE {id_key}={id}'
    mycursor.execute(Q)
    db.commit()

def login_user(username, passwd):
    msg_box = QMessageBox()
    msg_box.setFixedSize(400, 300)
    mycursor.execute(f'SELECT * FROM Users WHERE username=\'{username}\'')
    user = mycursor.fetchone()
    if user == None:
        return [-1, None]
    else:
            user_id, user_role, user_passwd = user[0], user[4], user[3]
    
    if user_passwd != passwd:
        return -2, None
    else:
        return 1, [user_id, user_role]

def get_all_accounts():
    mycursor.reset()
    mycursor.execute(f'SELECT id, username, passwd, role FROM Users')
    accounts = mycursor.fetchall()

    return accounts

def get_all_teachers():
    mycursor.reset()
    mycursor.execute(f'SELECT id, IdNumber, type, classId, subjectClassIds FROM Teachers')
    teachers = mycursor.fetchall()

    return teachers

def get_all_classes():
    mycursor.reset()
    mycursor.execute(f'SELECT id, className, teacherId FROM Classes')
    classes = mycursor.fetchall()

    return classes

def get_all_subject_classes():
    mycursor.reset()
    mycursor.execute(f'SELECT id, subjectName, teacherId, classId FROM SubjectClasses')
    teachers = mycursor.fetchall()
    return teachers

def get_all_subject_classes_same_teacher(teacher_id):
    mycursor.reset()
    mycursor.execute(f'SELECT id, subjectName, classId FROM SubjectClasses WHERE teacherId = {teacher_id}')
    subjectClasses = mycursor.fetchall()
    return subjectClasses

def get_all_students():
    mycursor.reset()
    mycursor.execute(f'SELECT id, classId FROM Students')
    students = mycursor.fetchall()
    return students

def get_my_students_from_class_id(class_id):
    mycursor.reset()
    mycursor.execute(f'SELECT id, classId FROM Students WHERE classId = {class_id}')
    students = mycursor.fetchall()
    return students

def update_user(id, new_username, new_passwd, new_role):
    mycursor.reset()
    mycursor.execute(f'UPDATE Users SET username = \'{new_username}\', passwd = \'{new_passwd}\', role = \'{new_role}\' WHERE id = {id}')
    db.commit()

def update_class(id, className, teacherId):
    if teacherId != -1:
        check_class_id = get_class_id_by_teacher_id_from_class(teacherId)
        if check_class_id == -1:
            exist_teacher_state = check_exist_teacher_by_teacher_id(teacherId)
            if exist_teacher_state == 1:
                teacher_type = get_teacher_type_by_teacher_id_from_teacher(teacherId)

                if teacher_type == '1':
                    mycursor.reset()
                    mycursor.execute(f'UPDATE Classes SET className = \'{className}\', teacherId = {teacherId} WHERE id = {id}')
                    db.commit()
                    return 1   
                else:
                    return -3
            else:
                return -2
        
        else:
            if check_class_id != id:
                return -1
            else:
                return 1
    else:
        mycursor.reset()
        mycursor.execute(f'UPDATE Classes SET className = \'{className}\', teacherId = {-1} WHERE id = {id}')
        db.commit()
        return 1   

def update_subject_class(id, subjectName, teacherId):
    mycursor.reset()
    mycursor.execute(f'UPDATE SubjectClasses SET subjectName = \'{subjectName}\', teacherId = {teacherId} WHERE id = {id}')
    db.commit()

def update_class_id_from_subject_class(subject_class_id, class_id):
    mycursor.reset()
    mycursor.execute(f'UPDATE SubjectClasses SET classId = {class_id} WHERE id = {subject_class_id}')
    db.commit()

def update_class_id_with_teacher_id(teacher_id, class_id):
    mycursor.reset()
    mycursor.execute(f'UPDATE Teachers SET classId = {class_id} WHERE id = {teacher_id}')
    db.commit()

def update_subject_class_id_with_teacher_id(teacher_id, subject_class_id):
    subject_class_ids_str = get_subject_class_ids_from_teacher(teacher_id)
    subject_class_ids = convert_string_to_list(subject_class_ids_str)
    subject_class_ids.append(subject_class_id)
    subject_class_ids_str = convert_list_to_string(subject_class_ids)

    mycursor.reset()
    mycursor.execute(f'UPDATE Teachers SET subjectClassIds = \'{subject_class_ids_str}\' WHERE id = {teacher_id}')
    db.commit()

def update_class_id_from_student(student_id, class_id):
    mycursor.reset()
    mycursor.execute(f'UPDATE Students SET classId = {class_id} WHERE id = {student_id}')
    db.commit()
    pass

def remove_subject_class_from_teacher(teacher_id, subject_class_id):
    subject_class_ids_str = get_subject_class_ids_from_teacher(teacher_id)
    subject_class_ids = convert_string_to_list(subject_class_ids_str)
    subject_class_ids.remove(subject_class_id)
    subject_class_ids_str = convert_list_to_string(subject_class_ids)

    mycursor.reset()
    mycursor.execute(f'UPDATE Teachers SET subjectClassIds = \'{subject_class_ids_str}\' WHERE id = {teacher_id}')
    db.commit()

def update_teacher_class_id_with_class_id(class_id, teacher_id):
    mycursor.reset()
    mycursor.execute(f'UPDATE Classes SET teacherId = {teacher_id} WHERE id = {class_id}')
    db.commit()

def update_info_user(id, passwd, name, gender, addr, phone, email):
    mycursor.reset()
    mycursor.execute(f'UPDATE Users SET passwd = \'{passwd}\', name = \'{name}\', gender = \'{gender}\', addr = \'{addr}\', phone = \'{phone}\', email = \'{email}\' WHERE id = {id}')
    db.commit()

def update_info_manager(id, idNumber):
    mycursor.reset()
    mycursor.execute(f'UPDATE Managers SET IdNumber = {idNumber} WHERE id = {id}')
    db.commit()

def update_info_teacher(id, idNumber):
    mycursor.reset()
    mycursor.execute(f'UPDATE Teachers SET IdNumber = {idNumber} WHERE id = {id}')
    db.commit()

def update_info_student(id, idNumber, grade, classId, schoolYear):
    mycursor.reset()
    mycursor.execute(f'UPDATE Students SET IdNumber = {idNumber}, grade = \'{grade}\', classId = {classId}, schoolYear = {schoolYear} WHERE id = {id}')
    db.commit()

def update_teachers_table(teacher_id, type, classId, newSubjectClassIds, oldSubjectClassIds):
    oldSubjectClassIds = convert_string_to_list(oldSubjectClassIds)
    newSubjectClassIds = convert_string_to_list(newSubjectClassIds)

    for oldSubjectClassId in oldSubjectClassIds:
        update_subject_class_teacher(oldSubjectClassId, -1)
        
    for newSubjectClassId in newSubjectClassIds:
        update_subject_class_teacher(newSubjectClassId, teacher_id)

    newSubjectClassIds = convert_list_to_string(newSubjectClassIds)
    mycursor.reset()
    mycursor.execute(f'UPDATE Teachers SET type = \'{type}\', classId = {classId}, subjectClassIds = \'{newSubjectClassIds}\' WHERE id = {teacher_id}')
    db.commit()

def update_subject_class_teacher(class_id, teacher_id):
    mycursor.reset()
    mycursor.execute(f'UPDATE SubjectClasses SET teacherId = {teacher_id} WHERE id = {class_id}')
    db.commit()

def update_subject_class_id_from_teacher(subject_class_id, teacher_id, type):
    oldSubjectClassIds = get_subject_class_ids_from_teacher(teacher_id)
    oldSubjectClassIds = convert_string_to_list(oldSubjectClassIds)
    if type == 'add':
        oldSubjectClassIds.append(subject_class_id)
    elif type == 'remove':
        oldSubjectClassIds.remove(subject_class_id)

    oldSubjectClassIds = convert_list_to_string(oldSubjectClassIds)

    mycursor.reset()
    mycursor.execute(f'UPDATE Teachers SET subjectClassIds = \'{oldSubjectClassIds}\' WHERE id = {teacher_id}')
    db.commit()

def update_score(subject_class_id, student_id, score):
    mycursor.reset()
    mycursor.execute(f'UPDATE Scores SET score = {score} WHERE subjectClassId={subject_class_id} AND studentId={student_id}')

    db.commit()

def create_score(subject_class_id, student_id, score):
    date_time = datetime.now()
    mycursor.reset()
    mycursor.execute("INSERT INTO Scores (subjectClassId, studentId, score, created) VALUES (%s,%s,%s,%s)", (subject_class_id, student_id, score, date_time))
    db.commit()


def get_score(subject_class_id, student_id):
    mycursor.reset()
    mycursor.execute(f'SELECT score FROM Scores WHERE subjectClassId={subject_class_id} AND studentId={student_id}')

    return mycursor.fetchone()

def get_info_user(id):
    mycursor.reset()
    mycursor.execute(f'SELECT * FROM Users WHERE id=\'{id}\'')
    return mycursor.fetchone()

def get_info_manager(id):
    mycursor.reset()
    mycursor.execute(f'SELECT * FROM Managers WHERE id=\'{id}\'')
    return mycursor.fetchone()

def get_info_teacher(id):
    mycursor.reset()
    mycursor.execute(f'SELECT * FROM Teachers WHERE id=\'{id}\'')
    return mycursor.fetchone()

def get_info_student(id):
    mycursor.reset()
    mycursor.execute(f'SELECT * FROM Students WHERE id=\'{id}\'')
    return mycursor.fetchone()

def get_subject_class_ids_from_teacher(teacher_id):
    mycursor.reset()
    mycursor.execute(f'SELECT subjectClassIds FROM Teachers WHERE id=\'{teacher_id}\'')
    return mycursor.fetchone()[0]

def get_students_in_same_class(class_id):
    mycursor.reset()
    mycursor.execute(f'SELECT id FROM Students WHERE classId = {class_id}')
    students = mycursor.fetchall()
    return students

def get_class_id_by_teacher_id_from_class(teacher_id):
    mycursor.reset()
    mycursor.execute(f'SELECT id FROM Classes WHERE teacherId={teacher_id}')

    try:
        return mycursor.fetchone()[0]
    except:
        return -1

def get_subject_classes_same_class(class_id):
    mycursor.reset()
    mycursor.execute(f'SELECT id, subjectName FROM SubjectClasses WHERE classId = {class_id}')
    subjectClasses = mycursor.fetchall()
    return subjectClasses

def get_score_by_subject_class_id_and_student_id(subject_class_id, student_id):
    mycursor.reset()
    mycursor.execute(f'SELECT score FROM Scores WHERE subjectClassId = {subject_class_id} AND studentId = {student_id}')
    try:
        return mycursor.fetchone()[0]
    except:
        return -1

def check_exist_teacher_by_teacher_id(teacher_id):
    mycursor.reset()
    mycursor.execute(f'SELECT id FROM Teachers WHERE id = {teacher_id}')

    try:
        mycursor.fetchone()[0]
        return 1
    except:
        return -1

def get_teacher_type_by_teacher_id_from_teacher(teacher_id):
    mycursor.reset()
    mycursor.execute(f'SELECT type FROM Teachers WHERE id = {teacher_id}')
    return mycursor.fetchone()[0]

def remove_user_by_id(id):
    mycursor.reset()
    mycursor.execute(f'SELECT role FROM Users WHERE id = {id}')
    role = mycursor.fetchone()[0]

    if role == '1':
        mycursor.reset()
        Q = f'DELETE FROM Manager WHERE id={id}'
        mycursor.execute(Q)


    elif role == '2':
        # update class
        mycursor.reset()
        mycursor.execute(f'UPDATE Classes SET teacherId = -1 WHERE teacherId = {id}')

        # update subject class
        mycursor.reset()
        mycursor.execute(f'UPDATE SubjectClasses SET teacherId = -1 WHERE teacherId = {id}')

        mycursor.reset()
        Q = f'DELETE FROM Teachers WHERE id={id}'
        mycursor.execute(Q)

    elif role == '3':
        mycursor.reset()
        Q = f'DELETE FROM Students WHERE id={id}'
        mycursor.execute(Q)


    mycursor.reset()
    Q = f'DELETE FROM Users WHERE id={id}'
    mycursor.execute(Q)

    db.commit()

def remove_class_by_id(id):
    mycursor.reset()
    Q = f'DELETE FROM Classes WHERE id={id}'
    mycursor.execute(Q)
    db.commit()

def remove_subject_class_by_id(id):
    mycursor.reset()
    Q = f'DELETE FROM SubjectClasses WHERE id={id}'
    mycursor.execute(Q)
    db.commit()



if __name__ == '__main__':
    create_account('admin', 'admin', '0')
    # show_table('UserInfos')
    # update_info_admin(5, '1', 'loc', 'O', 'none', 'none', 'none')


    # fetchone_account('Accounts', 'admin')

    pass