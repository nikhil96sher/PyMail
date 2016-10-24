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

CRLF = '\r\n'
TERMINATOR = CRLF + '.' + CRLF

def decode(input_str):
	result = ''
	search_result = re.search('=\?([^\?]*)\?([^\?]*)\?([^\?]*)\?=', input_str)
	while search_result is not None:
		charset, tp, text = search_result.groups()
		s = search_result.start(0)
		e = search_result.end(0)
		text = text.encode('cp866', 'ignore').decode('cp866', 'ignore')
		result += input_str[:s]
		input_str = input_str[e:].lstrip()
		if tp.lower() != 'q':
			result += base64.b64decode(text.encode('cp866')).decode(charset, 'ignore')
		else:
			result += quopri.decodestring(text).decode(charset, 'ignore')
		search_result = re.search('=\?([^\?]*)\?([^\?]*)\?([^\?]*)\?=', input_str)
	else:
		result += input_str
	return result

class pop3lib:

	message_list = []

	def send_message(self,m):
		logging.debug("\nC: "+m)
		self.sock.send((m + '\r\n').encode('utf-8'))

	def send_password(self,m):
		logging.debug("\nC: *********")
		self.sock.send((m + '\r\n').encode('utf-8'))

	def send_and_receiveline(self,mes):
		logging.debug("\nC: "+mes)
		self.sock.send((mes + '\r\n').encode('utf-8'))
		line = self.sock.recv(2048)
		logging.debug("\nS: " + line)
		return line
	
	def receiveline(self):
		line = self.sock.recv(2048)
		logging.debug("\nS: " + line)
		return line

	def receive_till_term(self, terminator):
		response = self.sock.recv(2048)
		while not response.endswith(TERMINATOR) and not response.endswith('.\r\n') and not response.endswith('.\r\n\r\n'):
			new_response = self.sock.recv(2048)
			response += new_response
			print new_response
		return response

	def get_message_count(self):
		self.send_message("list")
		mes = self.receive_till_term(TERMINATOR)
		cnt = len(mes.split('\r\n')) - 3
		return cnt

	def get_result(self,data):
		addr = 'No \'From: ...\''
		subj = 'No \'Subject: ...\''
		data = data.decode('cp866', 'ignore')
		from_data = re.search('^From:.*(.*\r?\n\s.*)*$', data, re.M | re.I)
		if from_data is not None:
			addr = decode(from_data.group(0))
		subj_data = re.search('^Subject:.*(.*\r?\n\s.*)*', data, re.M | re.I)
		if subj_data is not None:
			subj = decode(subj_data.group(0))
		return [subj, addr]

	def __init__(self, host_name, host_port, user_id, passw, log_level=logging.DEBUG):
		logging.basicConfig(format='%(levelname)s:%(message)s', level=log_level)
		try:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.sock = sock
			sock.connect((host_name, host_port))
			self.connection = True
		except Exception as e:
			print('can\'t connect to {0} on {1} port \r\n{3}'.format(host, port, e.__repr__()))
			self.connection = False
			return

		self.server_info = self.receiveline()
		auto = [
			'user {0}'.format(user_id),
			'pass {0}'.format(passw),
		]

		response = []
		for m in auto:
			self.send_password(m)
			response.append(self.receiveline())

		print response

		if response[0].find("+OK Name is a valid mailbox") != -1:
			self.username_valid = True
		else:
			self.username_valid = False

		if response[1].find("+OK Maildrop ready") != -1:
			self.password_valid = True
		else:
			self.password_valid = False

	def get_message_list(self):
		self.message_count = self.get_message_count()
		addr_list = []
		subj_list = []

		for message_number in range(1,self.message_count+1):
			self.send_message('top {0} 0'.format(message_number))
			# response = self.receive_till_term(TERMINATOR)

			response = self.sock.recv(2048)
			while not response.endswith(b'\r\n.\r\n'):
				response += self.sock.recv(2048)

			subj, addr = self.get_result(response)
			subj_list.append(subj)
			addr_list.append(addr)
			logging.info(('\nS: {0}\n{1}\n'.format(addr, subj)))
		return addr_list, subj_list


	def get_email_body(self, index):
		self.send_message("RETR "+str(index))
		response = self.receive_till_term(TERMINATOR)
		response = '\n'.join(response.split('\n')[1:])
		b = email.message_from_string(response)
		body = ""
		if b.is_multipart():
			for payload in b.get_payload():
				body = body + payload.get_payload()
		else:
			body = b.get_payload()
		body = body.replace("\r","")
		body = body[:-2]
		f =  open("message_retrieved.html","w")
		f.write(body)
		return body

if __name__ == "__main__":
	reload(sys)  
	sys.setdefaultencoding('utf8')
	pop_obj = pop3lib(HOST_ADDR,POP3_PORT,USERNAME,PASSWORD)
	# print pop_obj.get_message_list()
	# print pop_obj.get_email_body(14)
	# print "DONE"
