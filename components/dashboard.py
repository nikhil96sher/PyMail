# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI/login_dash.ui'
#
# Created: Wed Oct 26 03:38:40 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1262, 529)
        self.user_email = QtGui.QLabel(Form)
        self.user_email.setGeometry(QtCore.QRect(1030, 20, 221, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.user_email.setFont(font)
        self.user_email.setObjectName("user_email")
        self.retrieve_button = QtGui.QPushButton(Form)
        self.retrieve_button.setGeometry(QtCore.QRect(10, 50, 103, 34))
        self.retrieve_button.setObjectName("retrieve_button")
        self.compose_button = QtGui.QPushButton(Form)
        self.compose_button.setGeometry(QtCore.QRect(140, 50, 103, 34))
        self.compose_button.setObjectName("compose_button")
        self.received_email = QtGui.QTableWidget(Form)
        self.received_email.setGeometry(QtCore.QRect(10, 90, 821, 431))
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
        self.email_body.setGeometry(QtCore.QRect(840, 120, 411, 401))
        self.email_body.setObjectName("email_body")
        self.label = QtGui.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(930, 80, 91, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.app_title = QtGui.QLabel(Form)
        self.app_title.setGeometry(QtCore.QRect(10, 0, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setWeight(75)
        font.setBold(True)
        self.app_title.setFont(font)
        self.app_title.setObjectName("app_title")
        self.showing_label = QtGui.QLabel(Form)
        self.showing_label.setGeometry(QtCore.QRect(560, 60, 271, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.showing_label.setFont(font)
        self.showing_label.setObjectName("showing_label")
        self.open_browser = QtGui.QPushButton(Form)
        self.open_browser.setGeometry(QtCore.QRect(1100, 80, 151, 34))
        self.open_browser.setObjectName("open_browser")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.user_email.setText(QtGui.QApplication.translate("Form", "nik17.ucs2014@iitr.ac.in", None, QtGui.QApplication.UnicodeUTF8))
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
        self.showing_label.setText(QtGui.QApplication.translate("Form", "Showing 10 of 10,200 emails", None, QtGui.QApplication.UnicodeUTF8))
        self.open_browser.setText(QtGui.QApplication.translate("Form", "Open in Browser", None, QtGui.QApplication.UnicodeUTF8))

