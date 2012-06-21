#!/usr/bin/env python3
"""
	This is the base implementation of a player.
	It doesn't do anything, but it supports all
	of the possible player commands. It also implements
	the 'execute' command which provides easier, string-based
	access to the command functions.
"""

import socket

class PlayerBackend(object):
	def __init__(self, player_id, db):
		self.player_id = player_id
		self.db = db
		self.updatePlayer()
	def updatePlayer(self):
		x = self.db.SELECT('players', {'player_id': self.player_id})
		if x:
			self.player = x[0]
		else:
			self.player = None
	def start(self):
		pass
	def stop(self):
		pass
	def skip(self):
		pass
	def pause(self):
		pass
	def volume(self, volume):
		pass
	def zap(self, player):
		pass
	def execute(self, command, args):
		print("Updating player..")
		self.updatePlayer()
		print("Command = %s" % command)
		if command == "start":
			self.start()
		elif command == "stop":
			self.stop()
		elif command == "skip":
			self.skip()
		elif command == "pause":
			self.pause()
		elif command == "volume":
			if args:
				self.volume(args[0])
		elif command == "zap":
			if args:
				self.zap(args[0])
			else:
				print("Missing argument for command 'zap'")
		# Other commands might actually take more arguments
		# but you'd need to add them yourself
