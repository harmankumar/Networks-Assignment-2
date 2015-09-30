#!/usr/bin/env python
#author@Pranjal
#reference https://github.com/eliben/code-for-blog/blob/master/2011/socket_client_thread_sample

import socket
import sys
import threading
import Queue
from urlparse import urlparse
import os
import os.path

lock = Lock()

def write_to_file(path,response):
	file_name = os.path.basename(path)
	directory = s.path.dirname(path)
	lock.acquire()
	if not os.path.exists(directory):
    	os.makedirs(directory)
    lock.release()
    f = open(path,'w')
    for i in response:
    	f.write(i)

class Clientcmd(object):

	CONNECT , SEND , RECEIVE , CLOSE = range(4)

	def __inti(self,type,,data = None):
		self.type = type
		self.data = data

class Client(threading.Thread):

	def __init__(self,domain,Qreply=Queue.Queue(),Qcmd=Queue.Queue()):
		self.alive = threading.Event()
		self.alive.set()
		self.objectsNo = 0
		self.receive_buffer = 4096
		self.Qcmd = Qcmd
		self.Qreply = Qreply
		self.domain
		self.socket = socket.socket(
				socket.AF_INET, socket.SOCK_STREAM)
		self.socket.connect((self.domain, 80))

	def run(self):
		while self.alive.isSet():
			try:
				# Queue.get with timeout to allow checking self.alive
				url = self.Qcmd.get(True, 0.1)
				objectsNo += 1
				self.fetchURL(url)
			except Queue.Empty as e:
				continue
				
	def join(self, timeout=None):
		self.alive.clear()
		threading.Thread.join(self, timeout)

	def fetchURL(url):
		parsed = urlparse(url)
		domain = parsed.netloc
		path = parsed.path
		if(path == ""):
			path = "/"
		self.socket.sendall('GET %s HTTP/1.1\nHost: %s\nConnection: keep-alive\n\n' % (path,domain))

		response = [self.socket.recv(self.receive_buffer)]
		while response[-1]:
			response.append(self.socket.recv(self.receive_buffer))

		thread = Thread(target = write_to_file,args = (self.domain+path,response))
		thread.start()

		Qreply.put(self)

#initialize parameters
maxTCPperDomain = 1
maxOBJperTCP = 1

#exit if no input file
if(len(sys.argv) < 2):
	exit()

#assignments to parameters
input_list = sys.argv
input_file = input_list[1]
if(len(sys.argv) == 4):
	maxTCPperDomain = int(input_list[2])
	maxOBJperTCP = int(input_list[3])

print input_list

domains = {}
allConn = []
domainConnections = []


object_file = open(input_file,'r')
for line in object_file:
	url = line[1:-1].split(',')[1]
	parsed = urlparse(url)
	domain_name = socket.gethostbyname(parsed.netloc)
	if(domain_name in domains):
		try:
			#if some connection available
			clt = domainConnections[domains[domain_name]].get()
			clt.Qcmd.put(url)
		except Queue.Empty as e:
			if(len(allConn[domains[domain_name]]) < maxTCPperDomain):
				#open new conn
				clt = Client(domain_name,domainConnections[domains[domain_name]])
				allConn[domains[domain_name]].append(clt)
				clt.Qcmd.put(url)
			else:
				check_error = True
				for clt in allConn[domains[domain_name]]:
					if(clt.objectsNo < maxOBJperTCP):
						clt.Qcmd.put(url)
						check_error = False
						break
				if(check_error):
					print 'Invalid parameters'
					exit()
	else:
		#open new connection for new domain
		domains[domain_name] = len(domains)
		domainConnections.append(Queue.Queue())
		allConn.append([])
		clt = Client(domain_name,domainConnections[domains[domain_name]])
		allConn[domains[domain_name]].append(clt)
		clt.Qcmd.put(url)

#create an INET, STREAMing socket
#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#now connect to the web server on port 80
# - the normal http port
#s.connect(("www.mcmillan-inc.com", 80))



'''def helper_func(domain_name):
	clt = domainConnections[domains[domain_name]].get()
	if(clt.objectsNo < maxOBJperTCP):
		clt.Qcmd.put(url)
	else:
		helper_func()'''