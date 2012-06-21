#!/usr/bin/env python3
"""
	This tool will recursively scan a directory and
	add music in it to the database.
"""

import sys, os, subprocess

sys.path.append(os.path.dirname(sys.argv[0]) + '/lib')
from amp import db

tagreader = os.path.dirname(sys.argv[0]) + '/bin/tagreader'
DB = None

def readSong(path):
	global tagreader
	x = subprocess.check_output([tagreader, path])
	out = {}
	for i in x.splitlines():
		(attr, discard, value) = i.decode('utf-8').partition(":")
		out[attr] = value
	if "title" not in out:
		return None
	return out

def loadFile(song):
	global DB
	x = DB.SELECT("songs", {"path": song['path']})
	if x:
		DB.UpdateSong(x[0]['song_id'], song)
		print("Updated %s" % (song['path']))
	else:
		DB.AddSong(song)
		print("Added %s -> %s by %s" % (song['path'], song['title'], song['artist']))

if __name__ == "__main__":
	DB = db.Sqlite('/home/klange/Music/amp.sqlite')
	rootdir = sys.argv[1]
	for root, subFolders, files in os.walk(rootdir):
		for file in files:
			song = readSong(os.path.join(root, file))
			if song:
				loadFile(song)
			else:
				print("Not music: %s" % os.path.join(root,file))