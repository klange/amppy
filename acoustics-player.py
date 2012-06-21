#!/usr/bin/env python3
"""
	This is the player application called by remctl or
	through SSH; it is the replacement for the Perl command
	'acoustics' and provides the same functionality.
"""

import sys, os

sys.path.append(os.path.dirname(sys.argv[0]) + '/lib')
from amp import db, players

if __name__ == "__main__":
	# Arguments are [player] [command] [arguments]
	print(sys.argv)
	if len(sys.argv) < 2:
		print("Expected player_id")
		sys.exit(1)
	# And we expect at least a player and a command
	if len(sys.argv) < 3:
		print("Expected command")
		sys.exit(1)
	# XXX: Do configuration reading and check what player we should
	#      be using for this player_id and what database!
	from amp.players.mplayer import PlayerImpl
	player = PlayerImpl(sys.argv[1], db.Sqlite('/home/klange/Music/amp.sqlite'))
	# Execute the player command.
	player.execute(sys.argv[2], sys.argv[3:])
