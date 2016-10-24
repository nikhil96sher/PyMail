import logging
from conf import *
import email
import os
import sys
from socket import *
import base64
import time
import ssl
from email.base64mime import encode as encode_base64

CRLF = '\r\n.\r\n'
def send_email(SMTP_HOST, SMTP_PORT, USERNAME, PASSWORD, subject, fromaddr, toaddr, body):
	msg = "Subject: " + subject +"\r\n\r\n" + body
	endmsg = "\r\n.\r\n"

	# Choose a mail server (e.g. Google mail server) and call it mailserver
	mailserver = SMTP_HOST
	port = SMTP_PORT

	clientSocket = socket(AF_INET, SOCK_STREAM)
	#ssl_clientSocket = ssl.wrap_socket(clientSocket) 
	#ssl_clientSocket.connect((mailserver, port))
	clientSocket.connect((mailserver,port))
	ssl_clientSocket = clientSocket

	recv = ssl_clientSocket.recv(1024)
	print recv+"reci1997"

	# If the first three numbers of what we receive from the SMTP server are not
	# '220', we have a problem
	if recv[:3] != '220':
		print '220 reply not received from server.'

	stri = '%s %s%s' % ("AUTH", "PLAIN" + " " + encode_base64("\0%s\0%s" % (USERNAME, PASSWORD), eol=""), CRLF)
	print stri
	ssl_clientSocket.send(stri)
	recv = ssl_clientSocket.recv(1024)
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
	mailFromCommand = 'MAIL From: '+fromaddr+'\r\n'
	ssl_clientSocket.send(mailFromCommand)
	recv2 = ssl_clientSocket.recv(1024)
	print recv2

	# If the first three numbers of the response from the server are not
	# '250', we have a problem
	if recv2[:3] != '250':
		print '250 reply not received from server.'

	# Send RCPT TO command and print server response.
	rcptToCommand = 'RCPT To: '+toaddr+'\r\n'
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
	# subject = subject + "\r\n\r\n" 
	#ssl_clientSocket.send(subject)
	# date = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())
	# date = date + "\r\n\r\n"
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


if __name__ == "__main__":
	reload(sys)  
	sys.setdefaultencoding('utf8')
	# fromaddr = "admin"+"@iitr.ac.in"
	# toaddr = "anshulshah96"+"@gmail.com"
	toaddr = fromaddr = USERNAME+"@iitr.ac.in"
	send_email(HOST_ADDR,SMTP_PORT,USERNAME,PASSWORD,"test",fromaddr,toaddr,"TEST body")
	# pop_obj = pop3lib(HOST_ADDR,POP3_PORT,USERNAME,PASSWORD)
	# print pop_obj.get_message_list()
	# print pop_obj.get_email_body(14)
	# print "DONE"
