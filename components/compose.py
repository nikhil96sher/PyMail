# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI/compose.ui'
#
# Created: Wed Oct 26 02:49:07 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1302, 529)
        self.label = QtGui.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(540, 40, 201, 41))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.body = QtGui.QPlainTextEdit(Form)
        self.body.setGeometry(QtCore.QRect(240, 220, 831, 261))
        self.body.setObjectName("body")
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(240, 100, 71, 18))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(240, 140, 71, 18))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtGui.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(240, 180, 71, 18))
        self.label_4.setObjectName("label_4")
        self.send_email = QtGui.QPushButton(Form)
        self.send_email.setGeometry(QtCore.QRect(450, 490, 103, 34))
        self.send_email.setObjectName("send_email")
        self.discard_email = QtGui.QPushButton(Form)
        self.discard_email.setGeometry(QtCore.QRect(720, 490, 103, 34))
        self.discard_email.setObjectName("discard_email")
        self.app_title = QtGui.QLabel(Form)
        self.app_title.setGeometry(QtCore.QRect(0, 0, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setWeight(75)
        font.setBold(True)
        self.app_title.setFont(font)
        self.app_title.setObjectName("app_title")
        self.sender = QtGui.QLineEdit(Form)
        self.sender.setGeometry(QtCore.QRect(330, 90, 741, 32))
        self.sender.setObjectName("sender")
        self.receiver = QtGui.QLineEdit(Form)
        self.receiver.setGeometry(QtCore.QRect(330, 130, 741, 32))
        self.receiver.setObjectName("receiver")
        self.subject = QtGui.QLineEdit(Form)
        self.subject.setGeometry(QtCore.QRect(330, 170, 741, 32))
        self.subject.setObjectName("subject")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "Compose Email", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Form", "Sender", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Form", "Receiver", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Form", "Subject", None, QtGui.QApplication.UnicodeUTF8))
        self.send_email.setText(QtGui.QApplication.translate("Form", "Send", None, QtGui.QApplication.UnicodeUTF8))
        self.discard_email.setText(QtGui.QApplication.translate("Form", "Discard", None, QtGui.QApplication.UnicodeUTF8))
        self.app_title.setText(QtGui.QApplication.translate("Form", "PyMail", None, QtGui.QApplication.UnicodeUTF8))

