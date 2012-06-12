#!/usr/bin/env python3
# Acoustics Database Connection Manager

import sqlite3, random
import amp.song

class DatabaseManager(object):
	def __init__(self):
		self.conn = None
		pass
	def toDicts(self, rows):
		# Assume the default will do this for us.
		return rows
	def SELECT(self, what, arguments={}, order=False, direction="", limit=False, offset=False):
		c = self.conn.cursor()
		a = []
		query_string = "SELECT * FROM %s" % what
		if arguments:
			query_string += " WHERE "
			queries = []
			for i in arguments.keys():
				queries.append("%s = ?" % i)
				a.append(arguments[i])
			query_string += " AND ".join(queries)
		if order:
			query_string += " ORDER BY " + ", ".join(order)
		if direction:
			query_string += " " + direction
		if limit:
			query_string += " LIMIT ?"
			a.append(limit)
		if offset:
			query_string += " OFFSET ?"
			a.append(offset)
		print(query_string)
		c.execute(query_string, a)
		results = c.fetchall()
		return self.toDicts(results)
	def Search(self, args, limit=10, offset=0):
		c = self.conn.cursor()
		s = "%%%s%%" % (args)
		a = (s,s,s,s,limit,offset)
		c.execute('SELECT * FROM songs WHERE online = 1 AND (album LIKE ? OR artist LIKE ? OR title LIKE ? OR path LIKE ?) ORDER BY album, disc, track LIMIT ? OFFSET ?', a)
		results = c.fetchall()
		return self.toDicts(results)
	def QuickSearch(self, q, limit=10):
		c = self.conn.cursor()
		s = "%%%s%%" % (q)
		a = (s,s,s,limit)
		c.execute('SELECT title, album, artist FROM songs WHERE online = 1 AND (album LIKE ? OR artist LIKE ? OR title LIKE ?) GROUP BY album LIMIT ?', a)
		results = c.fetchall()
		return self.toDicts(results)
	def Random(self, limit=10):
		return self.SELECT("songs", {"online": 1}, order=["RAND()"], limit=limit)
	def History(self, voter=None, player="default", limit=10):
		c = self.conn.cursor()
		if voter:
			a = (voter, limit)
			c.execute("SELECT time FROM history WHERE voter = ? GROUP BY time ORDER BY time DESC LIMIT ?", a)
			results = c.fetchall()
			a = (results[-1]["time"], player, voter, limit)
			c.execute("SELECT history.who, history.time, songs.* FROM history INNER JOIN songs ON history.song_id = songs.song_id WHERE history.time >= ? AND history.player_id = ? AND WHERE voter = ? ORDER BY history.time DESC LIMIT ?", a)
			results = c.fetchall()
			return self.toDicts(results)
		else:
			a = (limit,)
			c.execute("SELECT time FROM history GROUP BY time ORDER BY time DESC LIMIT ?", a)
			results = c.fetchall()
			a = (results[-1]["time"], player, limit)
			c.execute("SELECT history.who, history.time, songs.* FROM history INNER JOIN songs ON history.song_id = songs.song_id WHERE history.time >= ? AND history.player_id = ? ORDER BY history.time DESC LIMIT ?", a)
			results = c.fetchall()
			return self.toDicts(results)
	def Recent(self, limit=20):
		return self.SELECT("songs", {"online": 1}, order=["song_id"], direction="DESC", limit=limit)
	def SongsByVotes(self, player=None):
		c = self.conn.cursor()
		a = (player,)
		c.execute("SELECT votes.who, votes.priority, votes.time, songs.* FROM votes INNER JOIN songs ON votes.song_id = songs.song_id WHERE votes.player_id = ? ORDER BY votes.priority", a)
		results = c.fetchall()
		return self.toDicts(results)

class Sqlite(DatabaseManager):
	def __init__(self, location="conf/acoustics.sqlite"):
		self.conn = sqlite3.connect(location)
		self.conn.row_factory = sqlite3.Row
	def toDicts(self, rows):
		output = []
		for i in rows:
			o = {}
			for k in i.keys():
				o[k] = i[k]
			output.append(o)
		return output
	def Random(self, limit=10):
		return self.SELECT("songs", {"online": 1}, order=["RANDOM()"], limit=limit)
