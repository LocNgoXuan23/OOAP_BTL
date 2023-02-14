from distutils.log import Log
import enum
from pydoc import classname
import sys
from turtle import update
from winsound import PlaySound
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QLabel, QMessageBox, QPushButton
from PyQt5.QtCore import QSize  
from PyQt5.uic import loadUi
from model import *
from controllers import *

class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()
        loadUi("LoginPage.ui", self)
        self.loginBtn.clicked.connect(self.loginFunction)

    def loginFunction(self):
        username = self.userNameInput.text()
        passwd = self.passwordInput.text()

        state, payload = login_user(username, passwd)
        msg_box = QMessageBox()
        msg_box.setFixedSize(400, 300)
        if state == -1:
            #self.alertLabel.setText('Not exist username !!')        
            msg_box.setText("Not exist username !!")
            msg_box.setWindowTitle("Error !!!")
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.exec_()
        elif state == -2:
            #self.alertLabel.setText('Password wrong !!')
            msg_box.setText("Password wrong !!")
            msg_box.setWindowTitle("Error !!!")
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.exec_()
        elif state == 1:
            user_id, user_role = payload
            
            if user_role == '0':
                adminHome = AdminHome(user_id)
                widget.addWidget(adminHome)
                widget.setCurrentIndex(widget.currentIndex() + 1)
            elif user_role == '1':
                managerHome = ManagerHome(user_id)
                widget.addWidget(managerHome)
                widget.setCurrentIndex(widget.currentIndex() + 1)
            elif user_role == '2':
                teacherHome = TeacherHome(user_id)
                widget.addWidget(teacherHome)
                widget.setCurrentIndex(widget.currentIndex() + 1)
            elif user_role == '3':
                studentHome = StudentHome(user_id)
                widget.addWidget(studentHome)
                widget.setCurrentIndex(widget.currentIndex() + 1)

            #print("Login successfully !!")
            msg_box.setText("Login successfully !!")
            msg_box.exec_()


class Register(QDialog):
    def __init__(self, user_id):
        super(Register, self).__init__()
        loadUi("registerPage.ui", self)
        self.user_id = user_id
        self.comeBackBtn.clicked.connect(self.backHome)
        self.registerBtn.clicked.connect(self.registerFunction)

    def backHome(self):
        adminHome = AdminHome(self.user_id)
        widget.addWidget(adminHome)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    
    def Function(self):
        msg_box = QMessageBox()
        msg_box.setFixedSize(400, 300)
        state = create_account(self.usernameInput.text(), self.passwordInput.text(), self.roleInput.text())

    def registerFunction(self):
        msg_box = QMessageBox()
        msg_box.setFixedSize(400, 300)
        state = create_account(self.usernameInput.text(), self.passwordInput.text(), self.roleInput.text())

        if state == 1:
            msg_box.setText("CREATE SUCCESSFULLY !!")
            msg_box.exec_()
            
class AdminHome(QDialog):
    def __init__(self, user_id):
        super(AdminHome, self).__init__()
        loadUi("adminHomePage.ui", self)
        self.user_id = user_id
        self.openRegisterBtn.clicked.connect(self.goToRegister)
        self.showAllAccountsBtn.clicked.connect(self.showAllAccounts)
        self.logoutBtn.clicked.connect(self.logout)
        self.openInfosBtn.clicked.connect(self.goToInfos)

    def goToRegister(self):
        register = Register(self.user_id)
        widget.addWidget(register)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    
    def showAllAccounts(self):
        showAllAccounts = ShowAllAccounts(self.user_id)
        widget.addWidget(showAllAccounts)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    
    def logout(self):
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    
    def goToInfos(self):
        userInfos = UserInfos(self.user_id)
        widget.addWidget(userInfos)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class ManagerHome(QDialog):
    def __init__(self, user_id):
        super(ManagerHome, self).__init__()
        loadUi("managerHome.ui", self)
        self.user_id = user_id
        self.logoutBtn.clicked.connect(self.logout)
        self.initComponent()
        self.openInfosBtn.clicked.connect(self.goToInfos)
        self.createClassBtn.clicked.connect(self.goToCreateClass)
        self.scheduleClassBtn.clicked.connect(self.goToScheduleClass)


    def logout(self):
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def initComponent(self):
        self.managerIdLabel.setText(f'Manager ID : {self.user_id}')

    def goToInfos(self):
        userInfos = UserInfos(self.user_id)
        widget.addWidget(userInfos)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goToCreateClass(self):
        createClass = CreateClass(self.user_id)
        widget.addWidget(createClass)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goToScheduleClass(self):
        scheduleClass = ScheduleClass(self.user_id)
        widget.addWidget(scheduleClass)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class TeacherHome(QDialog):
    def __init__(self, user_id):
        super(TeacherHome, self).__init__()
        loadUi("teacherHome.ui", self)
        self.user_id = user_id

        self.logoutBtn.clicked.connect(self.logout)
        self.openInfosBtn.clicked.connect(self.goToInfos)
        self.enterScoreBtn.clicked.connect(self.goToEnterScore)

        self.initComponent()

    def initComponent(self):
        self.user_infos = get_info_teacher(self.user_id)
        self.teacherType = self.user_infos[3]
        self.classId = self.user_infos[4]

        if self.teacherType == '1':
            self.classIdLabel.show()
            self.classIdLabel.setText(f'Home Class ID : {self.classId}')
            self.addStudentBtn.show()
            self.addStudentBtn.clicked.connect(self.goToAddStudent)

            self.showStudentScoresBtn.show()
            self.showStudentScoresBtn.clicked.connect(self.goToShowStudenScoresForHomeTeacher)
            
        elif self.teacherType == '0':
            self.classIdLabel.hide()
            self.addStudentBtn.hide()

            self.showStudentScoresBtn.hide()

        self.teacherTypeLabel.setText('Teacher Type : Chu Nghiem' if self.teacherType == '1' else 'Teacher Type : Bo mon')
        self.teacherIdLabel.setText(f'Teacher ID : {self.user_id}')

    
    def logout(self):
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goToInfos(self):
        userInfos = UserInfos(self.user_id)
        widget.addWidget(userInfos)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goToAddStudent(self):
        addStudent = AddStudent(self.user_id, self.classId)
        widget.addWidget(addStudent)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goToEnterScore(self):
        enterScore = EnterScore(self.user_id, self.classId)
        widget.addWidget(enterScore)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goToShowStudenScoresForHomeTeacher(self):
        showStudentScoresForHomeTeacher = ShowStudentScoresForHomeTeacher(self.user_id, self.classId)
        widget.addWidget(showStudentScoresForHomeTeacher)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class StudentHome(QDialog):
    def __init__(self, user_id):
        super(StudentHome, self).__init__()
        loadUi("studentHome.ui", self)
        self.user_id = user_id
        self.logoutBtn.clicked.connect(self.logout)
        self.openInfosBtn.clicked.connect(self.goToInfos)
        self.showScoresBtn.clicked.connect(self.goToShowScores)
        self.initComponent()

    def initComponent(self):
        self.user_infos = get_info_student(self.user_id)
        self.class_id = self.user_infos[3]

        self.studentIdLabel.setText(f'Student ID : {self.user_id}')
        self.classIdLabel.setText(f'Class ID : {self.class_id}')

    def logout(self):
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goToInfos(self):
        userInfos = UserInfos(self.user_id)
        widget.addWidget(userInfos)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goToShowScores(self):
        showScores = ShowScores(self.user_id, self.class_id)
        widget.addWidget(showScores)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class UserInfos(QDialog):
    def __init__(self, user_id):
        super(UserInfos, self).__init__()
        self.user_id = user_id
        loadUi("infosPage.ui", self)
        self.comeBackBtn.clicked.connect(self.backHome)
        self.updateInfosBtn.clicked.connect(self.updateInfos)

        self.user_infos = get_info_user(self.user_id)
        self.username = self.user_infos[2]
        self.passwd = self.user_infos[3]
        self.role = self.user_infos[4]
        self.name = self.user_infos[5]
        self.gender = self.user_infos[6]
        self.addr = self.user_infos[7]
        self.phone = self.user_infos[8]
        self.email = self.user_infos[9]

        if self.role == '1':
            _, _, self.idNumber = get_info_manager(self.user_id)
        elif self.role == '2':
            _, _, self.idNumber = get_info_teacher(self.user_id)
        elif self.role == '3':
            _, _, self.grade, self.classId, self.schoolYear, self.idNumber = get_info_student(self.user_id)

        self.initComponents()

    def backHome(self):
        if self.role == '0':
            adminHome = AdminHome(self.user_id)
            widget.addWidget(adminHome)
            widget.setCurrentIndex(widget.currentIndex() + 1)
        elif self.role == '1':
            managerHome = ManagerHome(self.user_id)
            widget.addWidget(managerHome)
            widget.setCurrentIndex(widget.currentIndex() + 1)
        elif self.role == '2':
            teacherHome = TeacherHome(self.user_id)
            widget.addWidget(teacherHome)
            widget.setCurrentIndex(widget.currentIndex() + 1)
        elif self.role == '3':
            studentHome = StudentHome(self.user_id)
            widget.addWidget(studentHome)
            widget.setCurrentIndex(widget.currentIndex() + 1)

    def initComponents(self):
        self.idLabel.setText(f'ID : {self.user_id}')
        self.roleLabel.setText(f'Role : {self.role}')
        self.usernameLabel.setText(f'{self.username}')
        self.passwordInput.setText(f'{self.passwd}')
        self.nameInput.setText(f'{self.name}')
        self.genderInput.setText(f'{self.gender}')
        self.addrInput.setText(f'{self.addr}')
        self.phoneInput.setText(f'{self.phone}')
        self.emailInput.setText(f'{self.email}')

        if self.role == '1':
            self.idNumberLabel.show()
            self.idNumberInput.show()
            self.idNumberInput.setText(str(self.idNumber))

            self.gradeLabel.hide()
            self.gradeInput.hide()
            self.classIdLabel.hide()
            self.classIdInput.hide()
            self.schoolYearLabel.hide()
            self.schoolYearInput.hide()
        
        elif self.role == '2':
            self.idNumberLabel.show()
            self.idNumberInput.show()
            self.idNumberInput.setText(str(self.idNumber))

            self.gradeLabel.hide()
            self.gradeInput.hide()
            self.classIdLabel.hide()
            self.classIdInput.hide()
            self.schoolYearLabel.hide()
            self.schoolYearInput.hide()
        
        elif self.role == '3':
            self.idNumberLabel.show()
            self.idNumberInput.show()
            self.gradeLabel.show()
            self.gradeInput.show()
            self.classIdLabel.show()
            self.classIdInput.show()
            self.schoolYearLabel.show()
            self.schoolYearInput.show()

            self.idNumberInput.setText(str(self.idNumber))
            self.gradeInput.setText(self.grade)
            self.classIdInput.setText(str(self.classId))
            self.schoolYearInput.setText(str(self.schoolYear))
        
        elif self.role == '0':
            self.idNumberLabel.hide()
            self.idNumberInput.hide()

            self.gradeLabel.hide()
            self.gradeInput.hide()
            self.classIdLabel.hide()
            self.classIdInput.hide()
            self.schoolYearLabel.hide()
            self.schoolYearInput.hide()

    def updateInfos(self):
        self.passwd = self.passwordInput.text()
        self.name = self.nameInput.text()
        self.gender = self.genderInput.text()
        self.addr = self.addrInput.text()
        self.phone = self.phoneInput.text()
        self.email = self.emailInput.text()

        update_info_user(self.user_id, self.passwd, self.name, self.gender, self.addr, self.phone, self.email)

        if self.role == '1':
            self.idNumber = self.idNumberInput.text()
            update_info_manager(self.user_id, int(self.idNumber))

        elif self.role == '2':
            self.idNumber = self.idNumberInput.text()
            update_info_teacher(self.user_id, int(self.idNumber))
        
        elif self.role == '3':
            self.idNumber = self.idNumberInput.text()
            self.grade = self.gradeInput.text()
            self.classId = self.classIdInput.text()
            self.schoolYear = self.schoolYearInput.text()
            update_info_student(self.user_id, int(self.idNumber), self.grade, int(self.classId), int(self.schoolYear))

class ShowAllAccounts(QDialog):
    def __init__(self, user_id):
        super(ShowAllAccounts, self).__init__()
        loadUi("showAllAccountsPage.ui", self)
        self.user_id = user_id
        self.comeBackBtn.clicked.connect(self.backHome)

        self.initComponent()
        self.accountsTable.setColumnWidth(0, 150)
        self.accountsTable.setColumnWidth(1, 150)
        self.accountsTable.setColumnWidth(2, 150)
        self.accountsTable.setColumnWidth(3, 150)
        self.loadAccountsList()
        self.updateAccountsTableBtn.clicked.connect(self.updateAccountsTable)
        self.removeAccountBtn.clicked.connect(self.removeAccount)
        self.accountsTable.selectionModel().selectionChanged.connect(self.selectTableChanged)

        self.selectedId = -1

    def initComponent(self):
        self.accounts = get_all_accounts()

    def backHome(self):
        adminHome = AdminHome(self.user_id)
        widget.addWidget(adminHome)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    
    def updateAccountsTable(self):
        for i, account in enumerate(self.accounts):
            id = int(self.accountsTable.item(i, 0).text())
            new_username = self.accountsTable.item(i, 1).text()
            new_passwd = self.accountsTable.item(i, 2).text()
            new_role = self.accountsTable.item(i, 3).text()
            update_user(id, new_username, new_passwd, new_role)
        
    def loadAccountsList(self):
        row = 0
        self.accountsTable.setRowCount(len(self.accounts))
        for account in self.accounts:
            self.accountsTable.setItem(row, 0, QtWidgets.QTableWidgetItem(f'{account[0]}'))
            self.accountsTable.setItem(row, 1, QtWidgets.QTableWidgetItem(account[1]))
            self.accountsTable.setItem(row, 2, QtWidgets.QTableWidgetItem(account[2]))
            self.accountsTable.setItem(row, 3, QtWidgets.QTableWidgetItem(account[3]))
            
            row += 1

    def selectTableChanged(self, selected):
        for ix in selected.indexes():
            id = self.accountsTable.item(ix.row(), 0).text()
            self.selectedId = id
            break

    def removeAccount(self):
        remove_user_by_id(self.selectedId)
        self.initComponent()
        self.loadAccountsList()

class CreateClass(QDialog):
    def __init__(self, user_id):
        super(CreateClass, self).__init__()
        loadUi("createClassPage.ui", self)
        self.user_id = user_id
        self.comeBackBtn.clicked.connect(self.backHome)
        self.initComponent()
        
        self.teachersTable.setColumnWidth(0, 100)
        self.teachersTable.setColumnWidth(1, 100)
        self.teachersTable.setColumnWidth(2, 100)
        self.teachersTable.setColumnWidth(3, 100)
        self.loadTeachersList()
        self.selectedTeacherId = -1
        self.selectedTeacherRow = -1
        
        self.classesTable.setColumnWidth(0, 100)
        self.classesTable.setColumnWidth(1, 100)
        self.classesTable.setColumnWidth(2, 100)
        self.loadClassesList()
        self.selectedClassId = -1
        self.selectedClassTeacherId = -1

        self.subjectClassesTable.setColumnWidth(0, 100)
        self.subjectClassesTable.setColumnWidth(1, 100)
        self.subjectClassesTable.setColumnWidth(2, 100)
        self.loadSubjectClassesList()
        self.selectedSubjectClassId = -1
        self.selectedSubjectClassTeacherId = -1


        self.createClassBtn.clicked.connect(self.createClass)
        self.createSubjectClassBtn.clicked.connect(self.createSubjectClass)
        self.teachersTable.selectionModel().selectionChanged.connect(self.selectTeachersTableChanged)
        self.classesTable.selectionModel().selectionChanged.connect(self.selectClassesTableChanged)
        self.subjectClassesTable.selectionModel().selectionChanged.connect(self.selectSubjectClassesTableChanged)
        self.updateTeachersTableBtn.clicked.connect(self.updateTeachersTable)
        self.removeClassBtn.clicked.connect(self.removeClass)
        self.updateClassesBtn.clicked.connect(self.updateClasses)

        self.removeRemoveClassBtn.clicked.connect(self.removeSubjectClass)
        self.updateSubjectClassesBtn.clicked.connect(self.updateSubjectClasses)



    def initComponent(self):
        self.user_infos = get_info_user(self.user_id)
        self.role = self.user_infos[4]
        self.teachers = get_all_teachers()
        self.classes = get_all_classes()
        self.subjectClasses = get_all_subject_classes()
    
    def selectTeachersTableChanged(self, selected):
        for ix in selected.indexes():
            id = self.teachersTable.item(ix.row(), 0).text()
            self.selectedTeacherId = id
            self.selectedTeacherRow = ix.row()
            break

    def selectClassesTableChanged(self, selected):
        for ix in selected.indexes():
            id = self.classesTable.item(ix.row(), 0).text()
            classTeacherId = self.classesTable.item(ix.row(), 2).text()
            self.selectedClassId = id
            self.selectedClassTeacherId = classTeacherId
            break

    def selectSubjectClassesTableChanged(self, selected):
        for ix in selected.indexes():
            id = self.subjectClassesTable.item(ix.row(), 0).text()
            subjectClassTeacherId = self.subjectClassesTable.item(ix.row(), 2).text()
            self.selectedSubjectClassId = id
            self.selectedSubjectClassTeacherId = subjectClassTeacherId
            break

    def updateTeachersTable(self):
        for i, teacher in enumerate(self.teachers):
            id = int(self.teachersTable.item(i, 0).text())

            newType = self.teachersTable.item(i, 1).text()
            oldType = self.teachers[i][2]

            newClassId = int(self.teachersTable.item(i, 2).text())
            newSubjectClassIds = self.teachersTable.item(i, 3).text()

            # oldClassId = self.teachers[i][3]
            oldSubjectClassIds = self.teachers[i][4]

            update_teachers_table(id, newType, newClassId, newSubjectClassIds, oldSubjectClassIds)

            if oldType != '0' and newType == '0':
                if newClassId != -1:
                    update_teacher_class_id_with_class_id(newClassId, -1)

        self.initComponent()
        self.loadClassesList()
        self.loadSubjectClassesList()
        self.loadTeachersList()

    def backHome(self):
        if self.role == '0':
            adminHome = AdminHome(self.user_id)
            widget.addWidget(adminHome)
            widget.setCurrentIndex(widget.currentIndex() + 1)
        elif self.role == '1':
            managerHome = ManagerHome(self.user_id)
            widget.addWidget(managerHome)
            widget.setCurrentIndex(widget.currentIndex() + 1)
        elif self.role == '2':
            teacherHome = TeacherHome(self.user_id)
            widget.addWidget(teacherHome)
            widget.setCurrentIndex(widget.currentIndex() + 1)
        elif self.role == '3':
            studentHome = StudentHome(self.user_id)
            widget.addWidget(studentHome)
            widget.setCurrentIndex(widget.currentIndex() + 1)

    def loadTeachersList(self):
        row = 0
        self.teachersTable.setRowCount(len(self.teachers))
        for teacher in self.teachers:
            teacher_id = teacher[0]

            class_id = get_class_id_by_teacher_id_from_class(teacher_id)

            self.teachersTable.setItem(row, 0, QtWidgets.QTableWidgetItem(f'{teacher[0]}'))
            self.teachersTable.setItem(row, 1, QtWidgets.QTableWidgetItem(f'{teacher[2]}'))
            self.teachersTable.setItem(row, 2, QtWidgets.QTableWidgetItem(f'{class_id}'))
            self.teachersTable.setItem(row, 3, QtWidgets.QTableWidgetItem(f'{teacher[4]}'))
            row += 1

    def loadClassesList(self):
        row = 0
        self.classesTable.setRowCount(len(self.classes))
        for class_item in self.classes:
            self.classesTable.setItem(row, 0, QtWidgets.QTableWidgetItem(f'{class_item[0]}'))
            self.classesTable.setItem(row, 1, QtWidgets.QTableWidgetItem(f'{class_item[1]}'))
            self.classesTable.setItem(row, 2, QtWidgets.QTableWidgetItem(f'{class_item[2]}'))
            row += 1

    def loadSubjectClassesList(self):
        row = 0
        self.subjectClassesTable.setRowCount(len(self.subjectClasses))
        for subject_class in self.subjectClasses:
            self.subjectClassesTable.setItem(row, 0, QtWidgets.QTableWidgetItem(f'{subject_class[0]}'))
            self.subjectClassesTable.setItem(row, 1, QtWidgets.QTableWidgetItem(f'{subject_class[1]}'))
            self.subjectClassesTable.setItem(row, 2, QtWidgets.QTableWidgetItem(f'{subject_class[2]}'))
            row += 1

    def createClass(self):
        state = create_class(self.classNameInput.text(), int(self.classTeacherIdInput.text()))
        if state == 1:
            print('Create class successfully !!')
            self.initComponent()
            self.loadClassesList()
            self.loadTeachersList()
            self.alertLabel.setText('Create class successfully !!')

        elif state == -1:
            self.alertLabel.setText(f'Giao Vien co ID {int(self.classTeacherIdInput.text())} da co lop')
            print(f'The teacher with ID {int(self.classTeacherIdInput.text())} has a class')

    def createSubjectClass(self):
        subject_class_id = create_subject_class(self.subjectNameInput.text(), int(self.subjectClassTeacherIdInput.text()))
        self.initComponent()
        self.loadSubjectClassesList()
        if int(self.subjectClassTeacherIdInput.text()) != -1:
            self.updateTeacherWithCreateSubjectClass(subject_class_id)

    def updateTeacherWithCreateSubjectClass(self, subject_class_id):
        update_subject_class_id_with_teacher_id(self.subjectClassTeacherIdInput.text(), subject_class_id)
        self.initComponent()
        self.loadTeachersList()

    def removeClass(self):
        remove_class_by_id(self.selectedClassId)
        self.initComponent()
        self.loadClassesList()

        # update teacher db
        update_class_id_with_teacher_id(self.selectedClassTeacherId, -1)
        self.initComponent()
        self.loadTeachersList()

    def removeSubjectClass(self):
        remove_subject_class_by_id(self.selectedSubjectClassId)
        self.initComponent()
        self.loadSubjectClassesList()

        print(self.selectedSubjectClassTeacherId)

        if self.selectedSubjectClassTeacherId != -1:
        # update teacher db
            remove_subject_class_from_teacher(self.selectedSubjectClassTeacherId, int(self.selectedSubjectClassId))
            self.initComponent()
            self.loadTeachersList()

    def updateClasses(self):
        for i, class_item in enumerate(self.classes):
            id = int(self.classesTable.item(i, 0).text())
            className = self.classesTable.item(i, 1).text()
            newTeacherId = int(self.classesTable.item(i, 2).text())

            state = update_class(id, className, newTeacherId)

            if state == 1:
                self.initComponent()
                self.loadTeachersList()
            
            elif state == -1:
                self.alertLabel.setText(f'The teacher with ID {newTeacherId} has a class')
                print(f'The teacher with ID {newTeacherId} has a class')
                break

            elif state == -2:
                self.alertLabel.setText(f'Teacher with ID {newTeacherId} not exist')
                print(f'Teacher with ID {newTeacherId} not exist')
                break
                
            elif state == -3:
                self.alertLabel.setText(f'Teacher with ID {newTeacherId} khong phai giao vien chu nghiem')
                print(f'Teacher with ID {newTeacherId} khong phai giao vien chu nghiem')
                break

        if i == len(self.classes)-1:
            self.alertLabel.setText('Update class successfully')
            print('Update class successfully')

    def updateSubjectClasses(self):
        for i, subject_class in enumerate(self.subjectClasses):
            id = int(self.subjectClassesTable.item(i, 0).text())
            subjectName = self.subjectClassesTable.item(i, 1).text()
            newTeacherId = int(self.subjectClassesTable.item(i, 2).text())
            oldTeacherId = int(self.subjectClasses[i][2])
            update_subject_class(id, subjectName, newTeacherId)
            if oldTeacherId != newTeacherId:
                if oldTeacherId != -1:
                    update_subject_class_id_from_teacher(id, oldTeacherId, 'remove')
                if newTeacherId != -1:
                    update_subject_class_id_from_teacher(id, newTeacherId, 'add')

        self.initComponent()
        self.loadTeachersList()
        
class ScheduleClass(QDialog):
    def __init__(self, user_id):
        super(ScheduleClass, self).__init__()
        loadUi("scheduleClass.ui", self)
        self.user_id = user_id
        self.comeBackBtn.clicked.connect(self.backHome)
        self.initComponent()

        self.classesTable.setColumnWidth(0, 100)
        self.classesTable.setColumnWidth(1, 100)
        self.loadClassesList()

        self.subjectClassesTable.setColumnWidth(0, 100)
        self.subjectClassesTable.setColumnWidth(1, 100)
        self.subjectClassesTable.setColumnWidth(2, 100)
        self.loadSubjectClassesList()

        self.updateSubjectClassesBtn.clicked.connect(self.updateSubjectClasses)


    def initComponent(self):
        self.user_infos = get_info_user(self.user_id)
        self.role = self.user_infos[4]
        self.classes = get_all_classes()
        self.subjectClasses = get_all_subject_classes()

    def backHome(self):
        managerHome = ManagerHome(self.user_id)
        widget.addWidget(managerHome)
        widget.setCurrentIndex(widget.currentIndex() + 1)


    def loadClassesList(self):
        row = 0
        self.classesTable.setRowCount(len(self.classes))
        for class_item in self.classes:
            self.classesTable.setItem(row, 0, QtWidgets.QTableWidgetItem(f'{class_item[0]}'))
            self.classesTable.setItem(row, 1, QtWidgets.QTableWidgetItem(f'{class_item[1]}'))
            row += 1

    def loadSubjectClassesList(self):
        row = 0
        self.subjectClassesTable.setRowCount(len(self.subjectClasses))
        for subject_class in self.subjectClasses:
            self.subjectClassesTable.setItem(row, 0, QtWidgets.QTableWidgetItem(f'{subject_class[0]}'))
            self.subjectClassesTable.setItem(row, 1, QtWidgets.QTableWidgetItem(f'{subject_class[1]}'))
            self.subjectClassesTable.setItem(row, 2, QtWidgets.QTableWidgetItem(f'{subject_class[3]}'))
            row += 1

    def updateSubjectClasses(self):
        for i, subject_class in enumerate(self.subjectClasses):
            id = int(self.subjectClassesTable.item(i, 0).text())
            classId = int(self.subjectClassesTable.item(i, 2).text())

            update_class_id_from_subject_class(id, classId)

class AddStudent(QDialog):
    def __init__(self, user_id, class_id):
        super(AddStudent, self).__init__()
        loadUi("addStudent.ui", self)
        self.user_id = user_id
        self.class_id = class_id
        self.comeBackBtn.clicked.connect(self.backHome)
        self.initComponent()

        self.myStudentsTable.setColumnWidth(0, 100)
        self.myStudentsTable.setColumnWidth(1, 100)
        self.loadMyStudentsTable()
        self.selectedMyStudentId = -1

        self.allStudentsTable.setColumnWidth(0, 100)
        self.allStudentsTable.setColumnWidth(1, 100)
        self.loadAllStudentsTable()
        self.selectedStudentId = -1

        self.allStudentsTable.selectionModel().selectionChanged.connect(self.selectAllStudentsTableChanged)
        self.myStudentsTable.selectionModel().selectionChanged.connect(self.selectMyStudentsTableChanged)
        self.updateStudentsTableBtn.clicked.connect(self.updateStudentsTable)
        self.addStudentBtn.clicked.connect(self.addStudent)
        self.removeStudentBtn.clicked.connect(self.removeStudent)

    def backHome(self):
        teacherHome = TeacherHome(self.user_id)
        widget.addWidget(teacherHome)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def initComponent(self):
        self.user_infos = get_info_teacher(self.user_id)
        self.classIdLabel.setText(f'Home Class ID : {self.class_id}')
        self.allStudents = get_all_students()
        self.myStudents = get_my_students_from_class_id(self.class_id)

    def selectAllStudentsTableChanged(self, selected):
        for ix in selected.indexes():
            id = self.allStudentsTable.item(ix.row(), 0).text()
            self.selectedStudentId = id
            break

    def selectMyStudentsTableChanged(self, selected):
        for ix in selected.indexes():
            id = self.myStudentsTable.item(ix.row(), 0).text()
            self.selectedMyStudentId = id
            break

    def updateStudentsTable(self):
        pass

    def loadAllStudentsTable(self):
        row = 0
        self.allStudentsTable.setRowCount(len(self.allStudents))
        for student in self.allStudents:
            self.allStudentsTable.setItem(row, 0, QtWidgets.QTableWidgetItem(f'{student[0]}'))
            self.allStudentsTable.setItem(row, 1, QtWidgets.QTableWidgetItem(f'{student[1]}'))
            row += 1

    def loadMyStudentsTable(self):
        row = 0
        self.myStudentsTable.setRowCount(len(self.myStudents))
        for student in self.myStudents:
            self.myStudentsTable.setItem(row, 0, QtWidgets.QTableWidgetItem(f'{student[0]}'))
            self.myStudentsTable.setItem(row, 1, QtWidgets.QTableWidgetItem(f'{student[1]}'))
            row += 1

    def addStudent(self):
        update_class_id_from_student(int(self.selectedStudentId), int(self.class_id))

        self.initComponent()
        self.loadAllStudentsTable()
        self.loadMyStudentsTable()
        print('ADD STUDENT')

    def removeStudent(self):
        update_class_id_from_student(int(self.selectedMyStudentId), -1)
        self.initComponent()
        self.loadAllStudentsTable()
        self.loadMyStudentsTable()
        print('REMOVE STUDENT')

class EnterScore(QDialog):
    def __init__(self, user_id, class_id):
        super(EnterScore, self).__init__()
        loadUi("enterScore.ui", self)
        self.user_id = user_id
        self.class_id = class_id
        self.initComponent()

        self.mySubjectClassesTable.setColumnWidth(0, 100)
        self.mySubjectClassesTable.setColumnWidth(1, 100)
        self.mySubjectClassesTable.setColumnWidth(2, 100)
        self.loadMySubjectClassesTable()
        self.selectedMySubjectclassesId = -1
        self.selectedMyclassesId = -1
        self.choosedMyClassesId = -1

        self.myStudentsTable.setColumnWidth(0, 100)
        self.myStudentsTable.setColumnWidth(1, 100)

        self.mySubjectClassesTable.selectionModel().selectionChanged.connect(self.selectMySubjectClassesTableChanged)
        self.comeBackBtn.clicked.connect(self.backHome)
        self.chooseBtn.clicked.connect(self.chooseSubjectClass)
        self.updateScoreBtn.clicked.connect(self.updateScore)


    def backHome(self):
        teacherHome = TeacherHome(self.user_id)
        widget.addWidget(teacherHome)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def initComponent(self):
        self.user_infos = get_info_teacher(self.user_id)
        self.classIdLabel.setText(f'Class ID : {self.class_id}')
        self.mySubjectClasses = get_all_subject_classes_same_teacher(int(self.user_id))

    def loadMySubjectClassesTable(self):
        row = 0
        self.mySubjectClassesTable.setRowCount(len(self.mySubjectClasses))
        for subject_class in self.mySubjectClasses:
            self.mySubjectClassesTable.setItem(row, 0, QtWidgets.QTableWidgetItem(f'{subject_class[0]}'))
            self.mySubjectClassesTable.setItem(row, 1, QtWidgets.QTableWidgetItem(f'{subject_class[1]}'))
            self.mySubjectClassesTable.setItem(row, 2, QtWidgets.QTableWidgetItem(f'{subject_class[2]}'))
            row += 1

    def loadMyStudentsTable(self):
        row = 0
        self.myStudentsTable.setRowCount(len(self.myStudents))
        for my_student in self.myStudents:
            self.myStudentsTable.setItem(row, 0, QtWidgets.QTableWidgetItem(f'{my_student[0]}'))

            score = get_score(int(self.choosedMyClassesId), int(my_student[0]))
            print(score)
            if score == None:
                create_score(int(self.choosedMyClassesId), int(my_student[0]), -1)
                score = -1
            else:
                score = score[0]
            

            self.myStudentsTable.setItem(row, 1, QtWidgets.QTableWidgetItem(f'{score}'))
            row += 1
        

    def selectMySubjectClassesTableChanged(self, selected):
        for ix in selected.indexes():
            id = self.mySubjectClassesTable.item(ix.row(), 0).text()
            class_id = self.mySubjectClassesTable.item(ix.row(), 2).text()
            self.selectedMySubjectclassesId = id
            self.selectedMyclassesId = class_id
            break

    def chooseSubjectClass(self):
        if self.selectedMyclassesId == '-1':
            self.myStudents = []
        else:
            self.myStudents = get_students_in_same_class(self.selectedMyclassesId)
            self.choosedMyClassesId = self.selectedMySubjectclassesId
        self.loadMyStudentsTable()
        print("CHOOSE CLASS")

    def updateScore(self):
        for i, student in enumerate(self.myStudents):
            student_id = int(self.myStudentsTable.item(i, 0).text())

            score = -1 if self.myStudentsTable.item(i, 1) == None else int(self.myStudentsTable.item(i, 1).text())

            print(int(self.choosedMyClassesId), int(student_id), score)

            update_score(int(self.choosedMyClassesId), int(student_id), score)

class ShowScores(QDialog):
    def __init__(self, user_id, class_id):
        super(ShowScores, self).__init__()
        loadUi("showScores.ui", self)
        self.user_id = user_id
        self.class_id = class_id
        self.comeBackBtn.clicked.connect(self.backHome)
        self.initComponent()

        self.scoresTable.setColumnWidth(0, 100)
        self.scoresTable.setColumnWidth(1, 100)
        self.scoresTable.setColumnWidth(1, 100)
        self.loadScoresTable()

    def backHome(self):
        studentHome = StudentHome(self.user_id)
        widget.addWidget(studentHome)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def initComponent(self):
        self.subject_classes = get_subject_classes_same_class(self.class_id)
        print(self.subject_classes)

    def loadScoresTable(self):
        row = 0
        self.scoresTable.setRowCount(len(self.subject_classes))
        for subject_class in self.subject_classes:
            score = get_score_by_subject_class_id_and_student_id(subject_class[0], self.user_id)

            self.scoresTable.setItem(row, 0, QtWidgets.QTableWidgetItem(f'{subject_class[0]}'))
            self.scoresTable.setItem(row, 1, QtWidgets.QTableWidgetItem(f'{subject_class[1]}'))
            self.scoresTable.setItem(row, 2, QtWidgets.QTableWidgetItem(f'{score}'))
            row += 1

class ShowStudentScoresForHomeTeacher(QDialog):
    def __init__(self, user_id, class_id):
        super(ShowStudentScoresForHomeTeacher, self).__init__()
        loadUi("showScoreForHomeTeacher.ui", self)
        self.user_id = user_id
        self.class_id = class_id
        self.comeBackBtn.clicked.connect(self.backHome)
        self.chooseBtn.clicked.connect(self.chooseSubjectClass)
        self.initComponent()

        self.subjectClassesTable.setColumnWidth(0, 100)
        self.subjectClassesTable.setColumnWidth(1, 100)
        self.loadSubjectClassesTable()
        self.selectedSubjectClassId = -1

        self.studentScoresTable.setColumnWidth(0, 100)
        self.studentScoresTable.setColumnWidth(1, 100)
        self.loadScoresTable()

        self.subjectClassesTable.selectionModel().selectionChanged.connect(self.selectSubjectClassesTableChanged)

    def backHome(self):
        teacherHome = TeacherHome(self.user_id)
        widget.addWidget(teacherHome)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def initComponent(self):
        self.subject_classes = get_subject_classes_same_class(self.class_id)
        self.my_students = get_my_students_from_class_id(self.class_id)

    def loadSubjectClassesTable(self):
        row = 0
        self.subjectClassesTable.setRowCount(len(self.subject_classes))
        for subject_class in self.subject_classes:
            self.subjectClassesTable.setItem(row, 0, QtWidgets.QTableWidgetItem(f'{subject_class[0]}'))
            self.subjectClassesTable.setItem(row, 1, QtWidgets.QTableWidgetItem(f'{subject_class[1]}'))
            row += 1

    def loadScoresTable(self):
        row = 0
        self.studentScoresTable.setRowCount(len(self.my_students))
        for my_student in self.my_students:
            self.studentScoresTable.setItem(row, 0, QtWidgets.QTableWidgetItem(f'{my_student[0]}'))
            if self.selectedSubjectClassId != -1:
                score = get_score_by_subject_class_id_and_student_id(self.selectedSubjectClassId, my_student[0])
                self.studentScoresTable.setItem(row, 1, QtWidgets.QTableWidgetItem(f'{score}'))
            row += 1

    def selectSubjectClassesTableChanged(self, selected):
        for ix in selected.indexes():
            self.selectedSubjectClassId = int(self.subjectClassesTable.item(ix.row(), 0).text())
            print(self.selectedSubjectClassId)
            break

    def chooseSubjectClass(self):
        self.initComponent()
        self.loadScoresTable()

if __name__ == "__main__":
    create_account('admin', 'admin', '0')

    app = QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()
    login = Login()
    widget.addWidget(login)
    widget.setFixedHeight(812)
    widget.setFixedWidth(1070)
    widget.show()

    try:
        sys.exit(app.exec_())
    except:
        print("Exit !!!")
   
