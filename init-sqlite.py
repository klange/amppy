#!/usr/bin/env python3
"""
	This is the player application called by remctl or
	through SSH; it is the replacement for the Perl command
	'acoustics' and provides the same functionality.
"""

import sys, os

sys.path.append(os.path.dirname(sys.argv[0]) + '/lib')
from amp import db, config

if __name__ == "__main__":
	conf = config.AcousticsConfig()
	DB = db.Sqlite(conf['database']['data_source'].split(":")[-1])
	DB.do("DROP TABLE IF EXISTS songs")
	DB.do("DROP TABLE IF EXISTS votes")
	DB.do("DROP TABLE IF EXISTS history")
	DB.do("DROP TABLE IF EXISTS players")
	DB.do("DROP TABLE IF EXISTS playlists")
	DB.do("DROP TABLE IF EXISTS playlist_contents")

	DB.do("""CREATE TABLE songs (song_id INTEGER PRIMARY KEY AUTOINCREMENT, path
	VARCHAR(1024) NOT NULL, artist VARCHAR(256), albumartist VARCHAR(256), album VARCHAR(256), title
	VARCHAR(256), disc INT, length INT NOT NULL, track INT, online
	TINYINT(1))""")

	DB.do("""CREATE TABLE votes (song_id INT, who VARCHAR(256), player_id
	VARCHAR(256), time INT, priority INT, UNIQUE(song_id, who))""")

	DB.do("""CREATE TABLE history (song_id INT, time TIMESTAMP, who
	VARCHAR(256), player_id VARCHAR(256))""")

	DB.do("""CREATE TABLE players (player_id VARCHAR(256), volume INT,
	song_id INT, song_start INT, local_id VARCHAR(256),
	remote_id VARCHAR(256), queue_hint TEXT, PRIMARY KEY(player_id))""")

	DB.do("""CREATE TABLE playlists (who VARCHAR(256) NOT NULL, playlist_id INTEGER
	PRIMARY KEY AUTOINCREMENT, title VARCHAR(256) NOT NULL)""")

	DB.do("""CREATE TABLE playlist_contents (playlist_id INT, song_id INT,
	priority INT, UNIQUE(playlist_id,song_id))""")



