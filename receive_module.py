import base64
import getpass
import re
import socket
import sys
import quopri
from conf import *
import logging
import email
# from email.parser import Parser

# in conf.py put
# username = --- 
# password = --- 

port = 110
login = username    
password = passw
host = host_addr
CRLF = '\r\n'

class pop3lib:

	message_list = []

	def send_message(self,m, s):
		logging.debug("\nC: "+m)
		s.send((m + '\r\n').encode('utf-8'))

	def send_password(self,m,s):
		logging.debug("\nC: *********")
		s.send((m + '\r\n').encode('utf-8'))

	def send_and_receiveline(self,mes,s):
		logging.debug("\nC: "+mes)
		s.send((mes + '\r\n').encode('utf-8'))
		line = s.recv(2048)
		logging.debug("\nS: " + line)
		return line
	
	def receiveline(self,s):
		line = s.recv(2048)
		logging.debug("\nS: " + line)
		return line

	def __init__(self, host_name, host_port, user_id, passw, log_level=logging.DEBUG):
		logging.basicConfig(format='%(levelname)s:%(message)s', level=log_level)
		try:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.connect((host_name, host_port))
		except Exception as e:
			print('can\'t connect to {0} on {1} port \r\n{3}'.format(host, port, e.__repr__()))
			sys.exit(0)

		# print sock.recv(2048)		

		self.server_info = self.receiveline(sock)
		auto = [
			'user {0}'.format(user_id),
			'pass {0}'.format(passw),
		]

		for m in auto:
			self.send_password(m, sock)

		print "DONE"
						
if __name__ == "__main__":
	reload(sys)  
	sys.setdefaultencoding('utf8')
	pop_obj = pop3lib(host,port,username,password)
