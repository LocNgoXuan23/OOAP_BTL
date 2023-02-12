# from main import *
# from distutils.log import Log
# import enum
# from pydoc import classname
# import sys
# from turtle import update
# from winsound import PlaySound
# from PyQt5 import QtWidgets
# from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QLabel
# from PyQt5.uic import loadUi
# from model import *
# from controllers import *

# class Login(QDialog):
#     def __init__(self):
#         super(Login, self).__init__()
#         loadUi("LoginPage.ui", self)
#         self.loginBtn.clicked.connect(self.loginFunction)

#     def loginFunction(self):
#         username = self.userNameInput.text()
#         passwd = self.passwordInput.text()

#         state, payload = login_user(username, passwd)
#         user_id, user_role = payload

#         if user_role == '0':
#             adminHome = AdminHome(user_id)
#             widget.addWidget(adminHome)
#             widget.setCurrentIndex(widget.currentIndex() + 1)
#         elif user_role == '1':
#             managerHome = ManagerHome(user_id)
#             widget.addWidget(managerHome)
#             widget.setCurrentIndex(widget.currentIndex() + 1)
#         elif user_role == '2':
#             teacherHome = TeacherHome(user_id)
#             widget.addWidget(teacherHome)
#             widget.setCurrentIndex(widget.currentIndex() + 1)
#         elif user_role == '3':
#             studentHome = StudentHome(user_id)
#             widget.addWidget(studentHome)
#             widget.setCurrentIndex(widget.currentIndex() + 1)