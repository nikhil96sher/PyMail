from PySide import QtCore, QtGui
from receive_module import *
import sender_module
import sys,os
from components import mainwindow,compose,login_dash
import conf
from PyQt4 import QtCore as QtCore2

class ControlMainWindow(QtGui.QMainWindow):	#Initialize New Window

	#Initial Function That Links Login Button Click To Login Function
	def __init__(self, parent=None):
		super(ControlMainWindow, self).__init__(parent)
		self.ui = mainwindow.Ui_MainWindow()
		self.ui.setupUi(self)
		self.start()
		self.ui.login_button.clicked.connect(self.login)

	#Set initial values of SMTP and POP3 Configurations
	def start(self):
		self.ui.smtp_port_value.setText(str(SMTP_PORT))
		self.ui.pop_port_value.setText(str(POP3_PORT))
		self.ui.smtp_host_value.setText(HOST_ADDR)
		self.ui.pop_host_value.setText(HOST_ADDR)
		self.ui.user_text.setText(USERNAME)
		self.ui.pass_text.setEchoMode(QtGui.QLineEdit.EchoMode.Password)
		self.ui.pass_text.setText(PASSWORD)

	#Login using pop3lib Function defined in receive_module
	def login(self):
		username = str(self.ui.user_text.text())
		password = str(self.ui.pass_text.text())
		smtp_host = str(self.ui.smtp_host_value.text())
		smtp_port = int(self.ui.smtp_port_value.text())
		pop_host = str(self.ui.pop_host_value.text())
		pop_port = int(self.ui.pop_port_value.text())

		pop_obj = pop3lib(pop_host, pop_port, username, password)

		#Sets the value of username,password,host and port in the pop_object which are used for retrieving and sending emails
		pop_obj.username = username
		pop_obj.password = password
		pop_obj.pop_host = pop_host
		pop_obj.pop_port = pop_port
		pop_obj.smtp_host = smtp_host
		pop_obj.smtp_port = smtp_port

		#Checks if the login is valid or not
		if not pop_obj.connection:
			message = "Connection Not Possible"
			self.ui.login_status.setText(message)
		elif not pop_obj.username_valid:
			message = "Incorrect Username"
			self.ui.login_status.setText(message)
		elif not pop_obj.password_valid:
			message = "Incorrect Password"
			self.ui.login_status.setText(message)
		else:
			message = "Login Successful"
			#Loads the Logged in Dashboard and Compose Dashboard in case the login is successful
			stackedWidget = QtGui.QStackedWidget()
			loginDash = LoginDashboard(self)
			composeDash  = ComposeDashboard(self)
			composeDash.initialize(pop_obj)
			loginDash.initialize(pop_obj)
			#Adds both the dashboards in the stack
			stackedWidget.insertWidget(0, loginDash)
			stackedWidget.insertWidget(1, composeDash)
			self.setCentralWidget(stackedWidget)

#Initializes the display with MainWindow
def gui_main():
	app = QtGui.QApplication(sys.argv)
	main_window = ControlMainWindow()
	main_window.show()
	sys.exit(app.exec_())

#LoginDashboard class
class LoginDashboard(QtGui.QWidget):
	#Initialization function that defines the control to listen to
	def __init__(self, parent=None):
		super(LoginDashboard, self).__init__(parent)
		self.ui = login_dash.Ui_Form()
		self.ui.setupUi(self)
		self.ui.received_email.cellClicked.connect(self.slotItemClicked)
		self.ui.compose_button.clicked.connect(self.compose)
		self.ui.retrieve_button.clicked.connect(self.retrieve)
		self.ui.open_browser.clicked.connect(self.open_in_browser)

	#Save the pop_obj and retrieve top 10 emails using get_message_list
	def initialize(self,pop_obj):
		self.pop_obj = pop_obj
		self.ui.user_email.setText(self.pop_obj.username)
		self.message_count = self.pop_obj.get_message_count()
		self.lastrow = self.ui.received_email.rowCount()
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
		self.ui.showing_label.setText("Showing "+str(self.lastrow)+" of "+str(self.message_count)+" emails")
		self.ui.received_email.resizeColumnsToContents()

	#Adds action to load the email data on click of table button
	def slotItemClicked(self,row,column):
		body = self.pop_obj.get_email_body(row)
		self.ui.email_body.setText(body)

	#Retrieve next 10 emails using get_message_list
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
		self.ui.showing_label.setText("Showing "+str(self.lastrow)+" of "+str(self.message_count)+" emails")
		self.ui.received_email.resizeColumnsToContents()

	#Cleans the string and removes trailing and leading whitespaces
	def clean(self,s):
		s = s.strip('\r\n')
		temp = s.split(':')[1:]
		s = ':'.join(temp)
		return s

	#Opens the email in a browser
	def open_in_browser(self):
		os.system("google-chrome message_retrieved.html")

	#Sets the currentStack state to Compose Page
	def compose(self):
		self.parent().setCurrentIndex(1)	#Change current top to Compose

#Compose Dashboard Class
class ComposeDashboard(QtGui.QWidget):
	#Initialization function that defines the controls to listen to
	def __init__(self, parent=None):
		super(ComposeDashboard,self).__init__(parent)
		self.ui = compose.Ui_Form()
		self.ui.setupUi(self)
		self.ui.send_email.clicked.connect(self.send_email)
		self.ui.discard_email.clicked.connect(self.discard)

	#Initializes the value of Sender and Receiver
	def initialize(self,pop_obj):
		self.pop_obj = pop_obj
		self.ui.sender.setText(pop_obj.username)
		self.ui.user_email.setText(pop_obj.username)

	#Sends an email using the data passed by the user
	def send_email(self):
		sender_module.send_email(self.pop_obj.smtp_host,self.pop_obj.smtp_port,
			self.pop_obj.username,self.pop_obj.password,self.ui.subject.text(),self.ui.sender.text(),self.ui.receiver.text(),self.ui.body.toPlainText())
		self.parent().setCurrentIndex(0)	#Change current top to Compose
		self.ui.sender.setText(self.pop_obj.username)
		self.ui.receiver.setText("")
		self.ui.subject.setText("")
		self.ui.body.clear()

	#Discards the data in the body, sender, receiver and subject fields and return to login_dash page
	def discard(self):
		self.parent().setCurrentIndex(0)
		self.ui.sender.setText(self.pop_obj.username)
		self.ui.receiver.setText(self.pop_obj.username)
		self.ui.subject.setText("")
		self.ui.body.clear()

#Runs the gui_main() function when the file is run from command line
if __name__ == "__main__":
	gui_main()
