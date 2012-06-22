#!/usr/bin/env python3

import os, subprocess
import amp.players.mplayer

class RPC(object):
	def execute(self, player_id, args):
		args.insert(0, player_id)
		if os.getcwd().endswith("/web"):
			args.insert(0, "../acoustics-player.py")
		else:
			args.insert(0, "./acoustics-player.py")
		subprocess.call(args)
