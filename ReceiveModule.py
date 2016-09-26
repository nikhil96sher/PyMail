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


def print_help():
    path = sys.argv[0].split("/")
    name = path[len(path) - 1]
    print("{0} host port".format(name))


def get_args():
    global port, host, login, password
    if len(sys.argv) == 1:
        print_help()
        sys.exit(0)
    else:
        host = sys.argv[1]
        if len(sys.argv) == 3:
            port = int(sys.argv[2])
    # login = input('LOGIN: ')
    # password = getpass.getpass('PASS: ')


def send_m(m, s):
    logging.debug("\nC: "+m)
    s.send((m + '\r\n').encode('utf-8'))

def send_and_receive(mes,s):
    # logging.debug("\nC: "+mes)
    s.send((mes + '\r\n').encode('utf-8'))
    print s.recv(2048)

def send_and_print(mes, s):
    # send_m(mes, s)
    logging.info(s.recv(2048).decode('utf-8'))


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


def get_result(data):
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

def RetrieveList(pop3_h, pop3_p, user_id, password, log_level):
    logging.basicConfig(format='%(levelname)s:%(message)s', level=log_level)
    global host, port, auto
    host = pop3_h
    port = pop3_p

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
    except Exception as e:
        print('can\'t connect to {0} on {1} port \r\n{3}'.format(host, port, e.__repr__()))
        sys.exit(0)
    logging.debug(sock.recv(1024))
    auto = [
        'user {0}'.format(login),
        'pass {0}'.format(password),
    ]

    for m in auto:
        send_and_receive(m, sock)
    print sock

    send_m('list', sock)
    mail_list = ''
    m = sock.recv(2048)
    while not m.endswith(b'\r\n.\r\n'):
        m = m.decode('utf-8')
        mail_list += m
        m = sock.recv(2048)
    mail_list += m.decode('utf-8')
    print mail_list
    messages = mail_list.split('\r\n')
    messages = messages[1: len(messages)]

    addr_list = []
    subj_list = []

    for m in messages:
        if m != '' and m != '.':
            number = m.split(' ')[0]
            send_m('top {0} 0'.format(number), sock)

            ans = sock.recv(2048)
            while not ans.endswith(b'\r\n.\r\n'):
                ans += sock.recv(2048)
            print ans
            subj, addr = get_result(ans)
            subj_list.append(subj)
            addr_list.append(addr)
            logging.info(('\nS: {0}\n{1}\n'.format(addr, subj)))
    return addr_list, subj_list

def RetrieveEmail(pop3_h, pop3_p, user_id, password, index, log_level):
    logging.basicConfig(format='%(levelname)s:%(message)s', level=log_level)
    global host, port, auto
    host = pop3_h
    port = pop3_p

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
    except Exception as e:
        print('can\'t connect to {0} on {1} port \r\n{3}'.format(host, port, e.__repr__()))
        sys.exit(0)
    logging.debug(sock.recv(1024))
    auto = [
        'user {0}'.format(login),
        'pass {0}'.format(password),
    ]

    for m in auto:
        send_and_receive(m, sock)

    send_m("RETR "+str(index), sock)
    mes1 = ''
    m=sock.recv(4096)
    while not m.endswith(b'.\r\n') and not m.endswith(b'.\r\n\r\n'):
        m = m.decode('utf-8')
        mes1 += m
        m = sock.recv(4096)
    mes1 += m.decode('utf-8')
    b = email.message_from_string(mes1)
    body = ""
    if b.is_multipart():
        for payload in b.get_payload():
            body = body + part.get_payload()
    else:
        body = b.get_payload()

    f =  open("message_retrieved.txt","w")
    f.write(mes1)
    return body

def main():
    global host, port, auto
    # get_args()
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
    except Exception as e:
        print('can\'t connect to {0} on {1} port \r\n{3}'.format(host, port, e.__repr__()))
        sys.exit(0)
    print(sock.recv(1024))
    auto = [
        'user {0}'.format(login),
        'pass {0}'.format(password),
    ]

    for m in auto:
        send_and_receive(m, sock)

    send_m('list', sock)
    mail_list = ''
    m = sock.recv(2048)
    while not m.endswith(b'\r\n.\r\n'):
        m = m.decode('utf-8')
        mail_list += m
        m = sock.recv(2048)
    mail_list += m.decode('utf-8')
    messages = mail_list.split('\r\n')
    messages = messages[1: len(messages)]

    for m in messages:
        if m != '' and m != '.':
            number = m.split(' ')[0]
            send_m('top {0} 0'.format(number), sock)

            ans = sock.recv(2048)
            while not ans.endswith(b'\r\n.\r\n'):
                ans += sock.recv(2048)

            subj, addr = get_result(ans)
            logging.info('\nS: {0}\n{1}\n'.format(addr, subj).encode('ascii', 'ignore').decode('ascii'))

    # send_m("RETR 11",sock)
    # mes1 = ''
    # m=sock.recv(4096)
    # while not m.endswith(b'.\r\n'):
    #     m = m.decode('utf-8')
    #     mes1 += m
    #     m = sock.recv(4096)
    # mes1 += m.decode('utf-8')
    # f =  open("message_retrieved.txt","w")
    # f.write(mes1)
    # print mes1

if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    reload(sys)  
    sys.setdefaultencoding('utf8')
    main()
