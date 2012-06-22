#!/usr/bin/env python3
"""
	This is the player application called by remctl or
	through SSH; it is the replacement for the Perl command
	'acoustics' and provides the same functionality.
"""

import sys, os, importlib

sys.path.append(os.path.dirname(sys.argv[0]) + '/lib')
from amp import db, config

if __name__ == "__main__":
	# Arguments are [player] [command] [arguments]
	if len(sys.argv) < 2:
		print("Expected player_id")
		sys.exit(1)
	# And we expect at least a player and a command
	if len(sys.argv) < 3:
		print("Expected command")
		sys.exit(1)
	conf = config.AcousticsConfig()
	if sys.argv[1] not in conf["{}"]['players'].split(","):
		sys.exit(1)
	player_module = importlib.import_module(conf.translate(conf['player.'+sys.argv[1]]["module"]))
	DB = db.Sqlite(conf['database']['data_source'].split(":")[-1])
	player = player_module.PlayerImpl(sys.argv[1], DB)
	# Execute the player command.
	player.execute(sys.argv[2], sys.argv[3:])
