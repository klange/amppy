#!/usr/bin/env python3

import os, signal, time, subprocess, sys
from amp.player import PlayerBackend

_thisPlayer = None

def _skip(signum, frame):
	self = _thisPlayer
	self.stopped = 0
	self.tell("quit\n")
	print("Skipping song...")

def _stop(signum, frame):
	self = _thisPlayer
	self.stopped = 1
	self.tell("quit\n")
	self.db.DeletePlayer(self.player_id)

def _pause(signum, frame):
	self = _thisPlayer
	self.tell("pause\n")

def _volume(signum, frame):
	self = _thisPlayer
	self.updatePlayer()
	self.tell("volume %d 1\n" % self.player["volume"])
	self.tell("get_volume\n")

class PlayerImpl(PlayerBackend):
	def start(self):
		"""
			To start a player instance for MPlayer, we fork to the background,
			set up the local id of the player to be our PID, and then start
			playing music through mplayer. We also maintain a pipe to our
			mplayer instance so we can safely quit, adjust volume, etc.
		"""
		if self.player:
			print("There seems to already be a player (with pid %d). Please try 'stop' before running 'start', or use 'zap' if that doesn't help things." % int(self.player["local_id"]))
			return
		pid = os.fork()
		if pid == 0:
			os.setsid()
			self.start_player()
			sys.exit(0)
		print("Started backgrounded player instance with PID#%d" % pid)
		return
	def zap(self, player):
		print("Zap! Deleting %s" % player)
		self.db.DeletePlayer(player)
	def start_player(self):
		self.pid = os.getpid()
		print("> I am the backgrounded process. My PID is %d" % self.pid)
		print("> My player_id is %s" % self.player_id)
		self.db.CreatePlayer(self.player_id, self.pid, 80)
		self.updatePlayer()

		while True:
			self.loop()

	def loop(self):
		global _thisPlayer
		_thisPlayer = self
		self.stopped = 0
		# XXX: Need to actually get the next song CORRECTLY!
		song = self.db.NextSong(self.player_id)
		start_time = time.time()
		self.db.UpdatePlayer(self.player_id, {
			"song_id": song["song_id"],
			"song_start": start_time
			})
		self.song_id = song["song_id"]
		print("Playing %s from PID... %d" % (song['path'], os.getpid()))
		self.mplayer = subprocess.Popen(['mplayer', '-slave', '-quiet', '-af', 'volnorm=2:0.10', '-volume', str(self.player['volume']), song['path']], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
		signal.signal(signal.SIGHUP, _skip)
		signal.signal(signal.SIGINT, _stop)
		signal.signal(signal.SIGUSR1, _volume)
		signal.signal(signal.SIGUSR2, _pause)
		print("Waiting for player to finish...")
		self.mplayer.wait()
		print("Player has finished.")
		if self.stopped:
			self.db.DeletePlayer(self.player_id)
			sys.exit(0)
		if 'who' in song:
			for i in song['who']:
				self.db.SetPlayed(self.song_id, self.player_id, i, start_time)
		self.db.DeleteVotes(self.song_id, self.player_id)

	def tell(self, string):
		self.mplayer.stdin.write(string.encode("utf-8"))

	def skip(self):
		self.send_signal(signal.SIGHUP)
	def stop(self):
		self.send_signal(signal.SIGINT)
	def pause(self):
		self.send_signal(signal.SIGUSR2)
	def volume(self, val):
		print("Setting volume to %d" % int(val))
		if int(val) < 0:
			val = 0
		elif int(val) > 100:
			val = 100
		self.db.UpdatePlayer(self.player_id, {'volume': int(val)})
		self.send_signal(signal.SIGUSR1)
	def send_signal(self, sig):
		if not self.player:
			return
		pid = int(self.player["local_id"])
		if not pid:
			return
		print("Sending signal %d to %d" % (sig, pid))
		os.kill(pid, sig)
