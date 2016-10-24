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

def receiveline(sock):
	line = sock.recv(1024)
	logging.debug("\nS: " + line)
	return line
def send_and_receiveline(mes, sock):
	logging.debug("\nC: "+mes)
	sock.send(mes)
	line = sock.recv(1024)
	logging.debug("\nS: " + line)
	return line	

def send_email(SMTP_HOST, SMTP_PORT, USERNAME, PASSWORD, subject, fromaddr, toaddr, body):
	print USERNAME, fromaddr, toaddr
	logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
	# msg = "Subject: " + subject +"\r\n\r\n" + body
	endmsg = "\r\n.\r\n"

	# Choose a mail server (e.g. Google mail server) and call it mailserver
	mailserver = SMTP_HOST
	port = SMTP_PORT

	sock = socket(AF_INET, SOCK_STREAM)
	sock.connect((mailserver,port))

	recv = receiveline(sock)
	# If the first three numbers of what we receive from the SMTP server are not '220', we have a problem
	if recv[:3] != '220':
		print '220 reply not received from server.'

	stri = '%s %s\r\n' % ("AUTH", "PLAIN" + " " + encode_base64("\0%s\0%s" % (USERNAME, PASSWORD), eol=""))
	recv = send_and_receiveline(stri, sock) 
		
	heloCommand = 'HELO Alice\r\n'
	recv1 = send_and_receiveline(heloCommand,sock)
	# If the first three numbers of the response from the server are not '250', we have a problem
	if recv1[:3] != '250':
		print '250 reply not received from server.'

	# Send MAIL FROM command and print server response.
	mailFromCommand = 'MAIL From: '+fromaddr+'\r\n'
	recv2 = send_and_receiveline(mailFromCommand, sock)
	# If the first three numbers of the response from the server are not '250', we have a problem
	if recv2[:3] != '250':
		print '250 reply not received from server.'

	# Send RCPT TO command and print server response.
	rcptToCommand = 'RCPT To: '+toaddr+'\r\n'
	recv3 = send_and_receiveline(rcptToCommand,sock)
	# If the first three numbers of the response from the server are not '250', we have a problem
	if recv3[:3] != '250':
		print '250 reply not received from server.'

	# Send DATA command and print server response.
	dataCommand = 'DATA\r\n'
	recv4 = send_and_receiveline(dataCommand,sock)
	# If the first three numbers of the response from the server are not '250', we have a problem
	if recv4[:3] != '354':
		print '354 reply not received from server.'

	# Send message data.
	# data = subject + "\r\n" 
	# date = "date: "time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())
	# data = data + date + "\r\n\r\n"
	# data = data + body + endmsg

	data = "Subject: " + subject +"\r\n\r\n" + body + endmsg
	# Final Message send
	line = send_and_receiveline(data,sock)

	# Send QUIT command and get server response.
	quitCommand = 'QUIT\r\n'
	recv5 = send_and_receiveline(quitCommand,sock)
	# If the first three numbers of the response from the server are not '250', we have a problem
	if recv5[:3] != '221':
		print '221 reply not received from server.'


if __name__ == "__main__":
	reload(sys)  
	sys.setdefaultencoding('utf8')
	# fromaddr = "admin"+"@iitr.ac.in"
	# toaddr = "anshulshah96"+"@gmail.com"
	toaddr = fromaddr = USERNAME
	send_email(HOST_ADDR,SMTP_PORT,USERNAME,PASSWORD,"test",fromaddr,toaddr,"TEST body")