#!/usr/bin/env python3
# Song Management Objects

import amp.db

class Song(object):
	def __init__(self, title="", artist="", album="", path="", sid=-1):
		self.title  = title
		self.artist = artist
		self.album  = album
		self.path   = path
		self.sid    = sid
	@staticmethod
	def fromDict(obj):
		pass
	def toDict(self):
		pass
