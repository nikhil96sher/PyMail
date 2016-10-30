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

# Searches for a particular Tag in raw message
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

	# sends a message m
	def send_message(self,m):
		logging.debug("\nC: "+m)
		self.sock.send((m + '\r\n').encode('utf-8'))

	# sends a message m without logging
	def send_password(self,m):
		logging.debug("\nC: *********")
		self.sock.send((m + '\r\n').encode('utf-8'))

	# sends a message mes and receives a line from socket
	def send_and_receiveline(self,mes):
		logging.debug("\nC: "+mes)
		self.sock.send((mes + '\r\n').encode('utf-8'))
		line = self.sock.recv(2048)
		logging.debug("\nS: " + line)
		return line

	# Receives a line from socket
	def receiveline(self):
		line = self.sock.recv(2048)
		logging.debug("\nS: " + line)
		return line

	# Receives until terminated
	def receive_till_term(self, terminator):
		response = self.sock.recv(2048)
		while not response.endswith(TERMINATOR) and not response.endswith('.\r\n') and not response.endswith('.\r\n\r\n'):
			new_response = self.sock.recv(2048)
			response += new_response
			print new_response
		return response

	# returns the total number of messages
	def get_message_count(self):
		self.send_message("list")
		mes = self.receive_till_term(TERMINATOR)
		cnt = len(mes.split('\r\n')) - 3
		return cnt

	# Parses the response to get Subject, Sender address and Date from raw message
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
		date_data = re.search('^Date:.*(.*\r?\n\s.*)*', data, re.M | re.I)
		if date_data is not None:
			date = decode(date_data.group(0))
		return [subj, addr, date]

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

	# returns back list of senders, subjects and date within the index LOWER_INDEX and UPPER_INDEX
	def get_message_list(self, LOWER_INDEX, UPPER_INDEX):
		addr_list = []
		subj_list = []
		date_list = []
		self.message_count = self.get_message_count()

		if(self.message_count - UPPER_INDEX <= 0):
			UPPER_INDEX = self.message_count - 1

		if(self.message_count - LOWER_INDEX <= 0):
			return addr_list, subj_list, date_list
		for message_number in range(self.message_count - LOWER_INDEX,self.message_count - UPPER_INDEX - 1,-1):
			self.send_message('top {0} 0'.format(message_number))
			# response = self.receive_till_term(TERMINATOR)
			response = self.sock.recv(2048)
			while not response.endswith(b'\r\n.\r\n'):
				response += self.sock.recv(2048)

			subj, addr, date = self.get_result(response)
			subj_list.append(subj)
			addr_list.append(addr)
			date_list.append(date)
			logging.info(('\nS: {0}\n{1}\n{2}\n'.format(addr, subj, date)))
		return addr_list, subj_list, date_list

	# returns the message body from message at position index
	def get_email_body(self, index):
		index = self.message_count - index
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
		f.close()
		return body

if __name__ == "__main__":
	reload(sys)
	sys.setdefaultencoding('utf8')
	pop_obj = pop3lib(HOST_ADDR,POP3_PORT,USERNAME,PASSWORD)
	print pop_obj.get_message_list(1,1)
	print pop_obj.get_email_body(14)
	print "DONE"
