# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI/login_dash.ui'
#
# Created: Wed Oct 26 02:49:07 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1305, 536)
        self.app_title_2 = QtGui.QLabel(Form)
        self.app_title_2.setGeometry(QtCore.QRect(1060, 20, 221, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.app_title_2.setFont(font)
        self.app_title_2.setObjectName("app_title_2")
        self.retrieve_button = QtGui.QPushButton(Form)
        self.retrieve_button.setGeometry(QtCore.QRect(20, 50, 103, 34))
        self.retrieve_button.setObjectName("retrieve_button")
        self.compose_button = QtGui.QPushButton(Form)
        self.compose_button.setGeometry(QtCore.QRect(150, 50, 103, 34))
        self.compose_button.setObjectName("compose_button")
        self.received_email = QtGui.QTableWidget(Form)
        self.received_email.setGeometry(QtCore.QRect(20, 100, 851, 421))
        self.received_email.setObjectName("received_email")
        self.received_email.setColumnCount(3)
        self.received_email.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.received_email.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.received_email.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.received_email.setHorizontalHeaderItem(2, item)
        self.email_body = QtGui.QTextBrowser(Form)
        self.email_body.setGeometry(QtCore.QRect(880, 110, 411, 411))
        self.email_body.setObjectName("email_body")
        self.label = QtGui.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(1060, 80, 71, 18))
        self.label.setObjectName("label")
        self.app_title = QtGui.QLabel(Form)
        self.app_title.setGeometry(QtCore.QRect(0, 0, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setWeight(75)
        font.setBold(True)
        self.app_title.setFont(font)
        self.app_title.setObjectName("app_title")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.app_title_2.setText(QtGui.QApplication.translate("Form", "nik17.ucs2014@iitr.ac.in", None, QtGui.QApplication.UnicodeUTF8))
        self.retrieve_button.setText(QtGui.QApplication.translate("Form", "Retrieve", None, QtGui.QApplication.UnicodeUTF8))
        self.compose_button.setText(QtGui.QApplication.translate("Form", "Compose", None, QtGui.QApplication.UnicodeUTF8))
        self.received_email.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("Form", "Sender", None, QtGui.QApplication.UnicodeUTF8))
        self.received_email.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("Form", "Date", None, QtGui.QApplication.UnicodeUTF8))
        self.received_email.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("Form", "Subject", None, QtGui.QApplication.UnicodeUTF8))
        self.email_body.setHtml(QtGui.QApplication.translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "Message", None, QtGui.QApplication.UnicodeUTF8))
        self.app_title.setText(QtGui.QApplication.translate("Form", "PyMail", None, QtGui.QApplication.UnicodeUTF8))

