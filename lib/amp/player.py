#!/usr/bin/env python3
# Client Library for Acoustics

import socket

class PlayerBackend(object):
	pass

class Messages():
	Messages.CONNECT = "CONN"
	Messages.QUIT    = "DISC"
	Messages.AUTH    = "AUTH"

class RemotePlayer(object):
	def __init__(self, server='localhost', port=6969):
		self._server = server #: Server hostname
		self._port   = port   #: Server port
		self._socket = None   #: Server socket
		self.user    = None   #: User attached to client
		pass
	def connect(self, server=False, port=False):
		if not server:
			server = self.server
		if not port:
			port   = self.port
		self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self._socket.connect((server,port))
		self.send(Messages.CONNECT)
	def send(self, message):
		self._socket.sendall(message + '\n')
