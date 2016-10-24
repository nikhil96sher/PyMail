from Tkinter import *
from ReceiveModule import *
import tkMessageBox
from sender import Mail
from sender import Message
import logging
from conf import *
from socket import *
import base64
import time
import ssl
from email.base64mime import encode as encode_base64
class Compose:

	def __init__(self, master, smtp_h,smtp_p,user_id,password):

		top = Toplevel(master)
		self.user_id = user_id
		self.password = password
		top.minsize(width=800, height=400)
		top.maxsize(width=800, height=400)
		Label(top, text="Sender Email ID").grid(row = 0,column = 0)
		Label(top, text="Receiver Email ID").grid(row = 1,column = 0)
		Label(top, text="Subject").grid(row = 2,column = 0)
		self.sender_id = StringVar(value=user_id)
		self.receiver_id = StringVar(value=user_id)
		self.subject = StringVar()
		Entry(top, textvariable=self.sender_id).grid(row = 0, column = 1)
		Entry(top, textvariable=self.receiver_id).grid(row = 1, column = 1)
		Entry(top, textvariable=self.subject).grid(row = 2, column = 1)
		Button(top, text="Send", command=self.send).grid(row = 3, column = 0)
		Button(top, text="Discard", command=top.destroy).grid(row=3, column =1)
		self.text = Text(top, height = 20, width = 60)
		self.text.grid(row=0, column=2, columnspan=1, rowspan=4, padx = 5)
	def send(self):
		print "Logging to " + self.user_id
		print "Sending from" + self.sender_id.get()
		print "Sending To" + self.receiver_id.get()
		'''mail = Mail("192.168.180.11", port=587, username=self.user_id, password=self.password,
			use_tls=False, use_ssl=False, debug_level=1)
		mail.send_message(self.subject.get(), fromaddr=self.sender_id.get(), to=self.receiver_id.get(), body=self.text.get("1.0",'end-1c'))'''
		#msg = Message(self.subject.get(), fromaddr=self.sender_id.get(), to=self.receiver_id.get(), body=self.text.get("1.0",'end-1c'))

		#print msg 

		msg = "\r\n " + self.text.get("1.0",'end-1c')
		endmsg = "\r\n.\r\n"

		# Choose a mail server (e.g. Google mail server) and call it mailserver
		mailserver = "192.168.180.11"
		port = 587

		# Create socket called clientSocket and establish a TCP connection with mailserver
		clientSocket = socket(AF_INET, SOCK_STREAM)
		#ssl_clientSocket = ssl.wrap_socket(clientSocket) 
		#ssl_clientSocket.connect((mailserver, port))
		clientSocket.connect((mailserver,port))
		ssl_clientSocket = clientSocket



		recv = ssl_clientSocket.recv(1024)
		print
		print recv+"reci1997"

		# If the first three numbers of what we receive from the SMTP server are not
		# '220', we have a problem
		if recv[:3] != '220':
			print '220 reply not received from server.'

		stri = '%s %s%s' % ("AUTH", "PLAIN" + " " + encode_base64("\0%s\0%s" % (self.user_id, self.password), eol=""), CRLF)
		print stri
		ssl_clientSocket.send(stri)
		recv = ssl_clientSocket.recv(1024)
		print
		print recv+"reci1997"
		
		heloCommand = 'HELO Alice\r\n'
		ssl_clientSocket.send(heloCommand)
		recv1 = ssl_clientSocket.recv(1024)
		print recv1

		# If the first three numbers of the response from the server are not
		# '250', we have a problem
		if recv1[:3] != '250':
		    print '250 reply not received from server.'

		# Send MAIL FROM command and print server response.
		mailFromCommand = 'MAIL From: '+self.sender_id.get()+'\r\n'
		ssl_clientSocket.send(mailFromCommand)
		recv2 = ssl_clientSocket.recv(1024)
		print recv2

		# If the first three numbers of the response from the server are not
		# '250', we have a problem
		if recv2[:3] != '250':
		    print '250 reply not received from server.'

		# Send RCPT TO command and print server response.
		rcptToCommand = 'RCPT To: '+self.receiver_id.get()+'\r\n'
		ssl_clientSocket.send(rcptToCommand)
		recv3 = ssl_clientSocket.recv(1024)
		print recv3

		# If the first three numbers of the response from the server are not
		# '250', we have a problem
		if recv3[:3] != '250':
		    print '250 reply not received from server.'

		# Send DATA command and print server response.
		dataCommand = 'DATA\r\n'
		ssl_clientSocket.send(dataCommand)
		recv4 = ssl_clientSocket.recv(1024)
		print recv4

		# If the first three numbers of the response from the server are not
		# '250', we have a problem
		if recv4[:3] != '250':
		    print '250 reply not received from server.'

		# Send message data.
		subject = self.subject.get()+" \r\n\r\n" 
		#ssl_clientSocket.send(subject)
		date = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())
		date = date + "\r\n\r\n"
		#ssl_clientSocket.send(date)
		ssl_clientSocket.send(msg)

		# Message ends with a single period.
		ssl_clientSocket.send(endmsg)

		# Send QUIT command and get server response.
		quitCommand = 'QUIT\r\n'
		ssl_clientSocket.send(quitCommand)
		recv5 = ssl_clientSocket.recv(1024)
		print recv5

		# If the first three numbers of the response from the server are not
		# '250', we have a problem
		if recv5[:3] != '221':
		    print '221 reply not received from server.'

class App:

	def __init__(self, master):
		self.master = master
		master.minsize(width=800, height=500)
		master.maxsize(width=800, height=500)
		self.smtp_h = StringVar(value="192.168.180.11")
		self.smtp_p = IntVar(value=587)
		self.pop3_h = StringVar(value="192.168.180.11")
		self.pop3_p = IntVar(value=110)
		self.user_id = StringVar(value="an9sh.ucs2014@iitr.ac.in")
		self.password = StringVar(value=passw)
		Label(master, text="SMTP Host").grid(row=0)
		Label(master, text="SMTP Port").grid(row=1)
		Label(master, text="POP3 Host").grid(row=2)
		Label(master, text="POP3 Port").grid(row=3)
		Label(master, text="Email Id").grid(row=4)
		Label(master, text="Password").grid(row=5)
		e1 = Entry(master, textvariable=self.smtp_h ,width=50).grid(row=0, column=1)
		e2 = Entry(master, textvariable=self.smtp_p ,width=50).grid(row=1, column=1)
		e3 = Entry(master, textvariable=self.pop3_h ,width=50).grid(row=2, column=1)
		e4 = Entry(master, textvariable=self.pop3_p ,width=50).grid(row=3, column=1)
		e5 = Entry(master, textvariable=self.user_id ,width=50).grid(row=4, column=1)
		e6 = Entry(master, textvariable=self.password , show="*",width=50).grid(row=5, column=1)

		self.lb = Listbox(master, name='lb', height = 20, width = 70)
		self.lb.bind('<<ListboxSelect>>', self.retrieve)
		self.lb.grid(row = 6, column = 0, rowspan = 10, columnspan = 2)
		self.text = Text(master, height = 30, width = 40, padx = 5, pady=5)
		self.text.grid(row=0, column=2, columnspan=3, rowspan=16)

		self.retrieve_button = Button(master, text="Retrieve Mails", command=self.retrieve_list)
		self.retrieve_button.grid(row=16,column=0)
		self.compose_button = Button(master, text="Compose", command=self.compose)
		self.compose_button.grid(row=16,column=1)
		self.quit_button = Button(master, text="QUIT", fg="red", command=master.quit)
		self.quit_button.grid(row=16,column=2)

	def compose(self):
		send_app = Compose(self.master, self.smtp_h.get(), self.smtp_p.get(), self.user_id.get(), self.password.get())
		# print "Logging to " + self.username.get() 
		# mail = Mail("192.168.180.11", port=587, username=self.user_id.get(), password=self.password.get(),
		# 	use_tls=False, use_ssl=False, debug_level=1)
		# mail.send_message("TEST Message", fromaddr=self.sender_id.get(), to=self.receiver_id.get(), body=self.message.get())

	def retrieve_list(self, lower_limit = 0, upper_limit = 10):
		addr_list, subj_list = RetrieveList(self.pop3_h.get(), self.pop3_p.get(), self.user_id.get(), self.password.get(), logging.DEBUG)
		self.lb.delete(0,self.lb.size()-1)
		for  i,a in enumerate(addr_list):
			addri =  addr_list[i].split(' ')[-1][:-1]
			subji = " ".join( subj_list[i].split(' ')[1:] )
			self.lb.insert(i+1,addri+" : "+subji)

		self.lb.activate(1)

	def retrieve(self, event):
		self.text.delete("1.0",END)
		w = event.widget
		index = int(w.curselection()[0])
		value = w.get(index)
		body = RetrieveEmail(self.pop3_h.get(), self.pop3_p.get(), self.user_id.get(), self.password.get(), index+1, logging.DEBUG)
		print body
		self.text.insert(INSERT, body)

if __name__ == "__main__":
	reload(sys)  
	sys.setdefaultencoding('utf8')
	root = Tk()
	app = App(root)
	root.mainloop()
	root.destroy() 