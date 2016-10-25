from PySide import QtCore, QtGui
from receive_module import *
import sender_module
import sys
from components import mainwindow,compose,login_dash
import conf
from PyQt4 import QtCore as QtCore2

class ControlMainWindow(QtGui.QMainWindow):
	def __init__(self, parent=None):
		super(ControlMainWindow, self).__init__(parent)
		self.ui = mainwindow.Ui_MainWindow()
		self.ui.setupUi(self)
		self.start()
		self.ui.login_button.clicked.connect(self.login)

	def start(self):
		self.ui.smtp_port_value.setText(str(SMTP_PORT))
		self.ui.pop_port_value.setText(str(POP3_PORT))
		self.ui.smtp_host_value.setText(HOST_ADDR)
		self.ui.pop_host_value.setText(HOST_ADDR)
		self.ui.user_text.setText(USERNAME)
		self.ui.pass_text.setEchoMode(QtGui.QLineEdit.EchoMode.Password)
		self.ui.pass_text.setText(PASSWORD)

	def login(self):
		username = str(self.ui.user_text.text())
		password = str(self.ui.pass_text.text())
		smtp_host = str(self.ui.smtp_host_value.text())
		smtp_port = int(self.ui.smtp_port_value.text())
		pop_host = str(self.ui.pop_host_value.text())
		pop_port = int(self.ui.pop_port_value.text())

		pop_obj = pop3lib(pop_host, pop_port, username, password)

		pop_obj.username = username
		pop_obj.password = password
		pop_obj.pop_host = pop_host
		pop_obj.pop_port = pop_port
		pop_obj.smtp_host = smtp_host
		pop_obj.smtp_port = smtp_port

		if not pop_obj.connection:
			message = "Connection Not Possible"
			self.ui.login_status.setText(QtGui.QApplication.translate("Form", message, None, QtGui.QApplication.UnicodeUTF8))
		elif not pop_obj.username_valid:
			message = "Incorrect Username"
			self.ui.login_status.setText(QtGui.QApplication.translate("Form", message, None, QtGui.QApplication.UnicodeUTF8))
		elif not pop_obj.password_valid:
			message = "Incorrect Password"
			self.ui.login_status.setText(QtGui.QApplication.translate("Form", message, None, QtGui.QApplication.UnicodeUTF8))
		else:
			message = "Login Successful"
			stackedWidget = QtGui.QStackedWidget()
			loginDash = LoginDashboard(self)
			composeDash  = ComposeDashboard(self)
			composeDash.initialize(pop_obj)
			loginDash.initialize(pop_obj)
			stackedWidget.insertWidget(0, loginDash)
			stackedWidget.insertWidget(1, composeDash)
			self.setCentralWidget(stackedWidget)

def gui_main():
	app = QtGui.QApplication(sys.argv)
	main_window = ControlMainWindow()
	main_window.show()
	sys.exit(app.exec_())

class ComposeDashboard(QtGui.QWidget):
	def __init__(self, parent=None):
		super(ComposeDashboard,self).__init__(parent)
		self.ui = compose.Ui_Form()
		self.ui.setupUi(self)
		self.ui.send_email.clicked.connect(self.send_email)
		self.ui.discard_email.clicked.connect(self.discard)

	def initialize(self,pop_obj):
		self.pop_obj = pop_obj
		self.ui.sender.setText(pop_obj.username)
		self.ui.receiver.setText(pop_obj.username)

	def send_email(self):
		sender_module.send_email(self.pop_obj.smtp_host,self.pop_obj.smtp_port,
			self.pop_obj.username,self.pop_obj.password,self.ui.subject.text(),self.ui.sender.text(),self.ui.receiver.text(),self.ui.body.toPlainText())
		self.parent().setCurrentIndex(0)	#Change current top to Compose
		self.ui.sender.setText(self.pop_obj.username)
		self.ui.receiver.setText(self.pop_obj.username)
		self.ui.subject.setText("")
		self.ui.body.clear()

	def discard(self):
		self.parent().setCurrentIndex(0)
		self.ui.sender.setText(self.pop_obj.username)
		self.ui.receiver.setText(self.pop_obj.username)
		self.ui.subject.setText("")
		self.ui.body.clear()

class LoginDashboard(QtGui.QWidget):
	def __init__(self, parent=None):
		super(LoginDashboard, self).__init__(parent)
		self.ui = login_dash.Ui_Form()
		self.ui.setupUi(self)
		self.ui.received_email.cellClicked.connect(self.slotItemClicked)
		self.ui.compose_button.clicked.connect(self.compose)
		self.ui.retrieve_button.clicked.connect(self.retrieve)

	def initialize(self,pop_obj):
		self.pop_obj = pop_obj
		self.message_count = self.pop_obj.get_message_count()
		self.lastrow = self.ui.received_email.rowCount()
		senders,subjects,dates = self.pop_obj.get_message_list(self.lastrow,self.lastrow+10)
		for sender,subject,date in zip(senders,subjects,dates):
			self.ui.received_email.insertRow(self.lastrow)
			send = QtGui.QTableWidgetItem(sender[:-1])
			date = QtGui.QTableWidgetItem(date[:-1])
			sub = QtGui.QTableWidgetItem(subject[:-1])
			self.ui.received_email.setItem(self.lastrow,0,send)
			self.ui.received_email.setItem(self.lastrow,1,date)
			self.ui.received_email.setItem(self.lastrow,2,sub)
			self.lastrow+=1

	def slotItemClicked(self,row,column):
		body = self.pop_obj.get_email_body(row)
		self.ui.email_body.setText(body)

	def retrieve(self):
		senders,subjects,dates = self.pop_obj.get_message_list(self.lastrow,self.lastrow+10)
		for sender,subject,date in zip(senders,subjects,dates):
			self.ui.received_email.insertRow(self.lastrow)
			send = QtGui.QTableWidgetItem(self.clean(sender))
			date = QtGui.QTableWidgetItem(self.clean(date))
			sub = QtGui.QTableWidgetItem(self.clean(subject))
			self.ui.received_email.setItem(self.lastrow,0,send)
			self.ui.received_email.setItem(self.lastrow,1,date)
			self.ui.received_email.setItem(self.lastrow,2,sub)
			self.lastrow+=1

	def clean(self,s):
		s = s.strip('\r\n')
		temp = s.split(':')[1:]
		s = ':'.join(temp)
		return s

	def compose(self):
		self.parent().setCurrentIndex(1)	#Change current top to Compose

if __name__ == "__main__":
	gui_main()
