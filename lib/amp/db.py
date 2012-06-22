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
	def SELECT(self, what, arguments={}, order=False, direction="", limit=False, offset=False, where="AND", comparator="="):
		c = self.conn.cursor()
		a = []
		query_string = "SELECT * FROM %s" % what
		if arguments:
			query_string += " WHERE "
			queries = []
			for i in arguments.keys():
				queries.append("%s %s ?" % (i, comparator))
				a.append(arguments[i])
			query_string += (" %s " % where).join(queries)
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
			c.execute("SELECT history.who, history.time, songs.* FROM history INNER JOIN songs ON history.song_id = songs.song_id WHERE history.time >= ? AND history.player_id = ? AND WHERE history.who = ? ORDER BY history.time DESC LIMIT ?", a)
			results = c.fetchall()
			return self.toDicts(results)
		else:
			a = (limit,)
			c.execute("SELECT time FROM history GROUP BY time ORDER BY time DESC LIMIT ?", a)
			results = c.fetchall()
			a = (results[-1]["time"], player, limit)
			c.execute("SELECT history.who, history.time, songs.* FROM history INNER JOIN songs ON history.song_id = songs.song_id WHERE history.time >= ? AND history.player_id = ? ORDER BY history.time DESC LIMIT ?", a)
			results = self.toDicts(c.fetchall())
			output = {}
			for i in results:
				if i['time'] not in output:
					i['who'] = [i['who']]
					output[i['time']] = i
				else:
					output[i['time']]['who'].append(i['who'])
			# Back to a list
			results = []
			for k,v in output.items():
				results.append(v)
			return results
	def Recent(self, limit=20):
		return self.SELECT("songs", {"online": 1}, order=["song_id"], direction="DESC", limit=limit)
	def SongsByVotes(self, player=None):
		c = self.conn.cursor()
		c.execute("SELECT votes.who, votes.priority, votes.time, songs.* FROM votes INNER JOIN songs ON votes.song_id = songs.song_id WHERE votes.player_id = ? ORDER BY votes.priority", [player])
		return self.toDicts(c.fetchall())
	def TopVoted(self, limit=20):
		c = self.conn.cursor()
		c.execute('SELECT title, history.song_id, COUNT(history.song_id) FROM history, songs WHERE songs.song_id = history.song_id GROUP BY history.song_id ORDER BY COUNT(history.song_id) DESC LIMIT ?', [limit])
		return self.toDicts(c.fetchall())
	def AlbumSearch(self, keyword=""):
		c = self.conn.cursor()
		s = "%%%s%%" % (keyword)
		c.execute('SELECT album, song_id FROM songs WHERE (album LIKE ? OR artist LIKE ?) AND online = 1 GROUP BY album', [s,s]);
		return self.toDicts(c.fetchall())
	def Select(self, field, value, mode="select"):
		c = self.conn.cursor()
		if mode == "search":
			value = "%%%s%%" % value
			comparator = "LIKE"
		else:
			comparator = "="
		if field == "any":
			where = "OR"
			args  = {"artist": value, "album": value, "title": value, "path": value}
		else:
			where = "AND"
			if field in ["artist", "album", "title", "path"]:
				args = {field: value}
			else:
				return []
		return self.SELECT("songs", args, where=where, comparator=comparator, order=["album", "track"])
	def NextVote(self, user, player):
		c = self.conn.cursor()
		c.execute("SELECT max(priority) FROM votes WHERE who = ? AND player_id = ?", [user, player])
		v = c.fetchall()
		if len(v) and not v[0]["max(priority)"] is None:
			return v[0]["max(priority)"] + 1
		else:
			return 0
	def NumVotes(self, user, player):
		c = self.conn.cursor()
		c.execute("SELECT count(*) FROM votes WHERE who = ? AND player_id = ?", [user, player])
		v = c.fetchall()
		if len(v):
			return self.toDicts(v)[0]["count(*)"]
		else:
			return 0
	def AddVote(self, user, player, song, priority):
		c = self.conn.cursor()
		c.execute("INSERT IGNORE INTO votes (song_id, time, player_id, who, priority) VALUES (?, now(), ?, ?, ?)", [song, player, user, priority])
		self.conn.commit()
	def Unvote(self, user, song):
		c = self.conn.cursor()
		c.execute("DELETE FROM votes WHERE song_id = ? AND who = ?", [song, user])
		self.conn.commit()
	def DeleteVotes(self, song, player):
		c = self.conn.cursor()
		c.execute("DELETE FROM votes WHERE player_id = ? AND song_id = ?", [player, song])
		self.conn.commit()
	def SetPlayed(self, song, player, who, time):
		c = self.conn.cursor()
		c.execute("INSERT INTO history (song_id, player_id, who, time) VALUES (?, ?, ?, ?)", [song, player, who, time])
		self.conn.commit()
	def SongCount(self):
		c = self.conn.cursor()
		c.execute("SELECT count(*) FROM SONGS",[])
		v = c.fetchall()
		if len(v):
			return self.toDicts(v)[0]["count(*)"]
		else:
			return 0
	def TopArtists(self, who=None, limit=10):
		c = self.conn.cursor()
		if who:
			c.execute("SELECT artist, count(songs.artist) AS count FROM songs, history WHERE songs.song_id = history.song_id AND history.who = ? GROUP BY artist ORDER BY count(songs.artist) DESC LIMIT ?", [who, limit])
		else:
			c.execute("SELECT artist, count(songs.artist) AS count FROM songs, history WHERE songs.song_id = history.song_id GROUP BY artist ORDER BY count(songs.artist) DESC LIMIT ?", [limit])
		return self.toDicts(c.fetchall())
	def Playlists(self, who="", title=""):
		s = "%%%s%%" % title
		return self.SELECT("playlists", {"who": who, "title": s}, comparator="LIKE")
	def PlaylistsLoose(self, value):
		s = "%%%s%%" % value
		return self.SELECT("playlists", {"who": s, "title": s}, where="OR", comparator="LIKE")
	def PlaylistContents(self, playlist_id):
		c = self.conn.cursor()
		c.execute("SELECT songs.* FROM playlist_contents INNER JOIN songs ON playlist_contents.song_id = songs.song_id WHERE online = 1 AND playlist_id = ? ORDER BY priority", [playlist_id])
		return self.toDicts(c.fetchall())
	def PlaylistInfo(self, playlist_id):
		x = self.SELECT("playlists", {"playlist_id": playlist_id})
		if len(x):
			return x[0]
		else:
			return None
	def NextPlaylistSong(self, playlist_id):
		c = self.conn.cursor()
		c.execute("SELECT max(priority) FROM playlist_contents WHERE playlist_id = ?", [playlist_id])
		v = c.fetchall()
		if len(v) and not v[0]["max(priority)"] is None:
			return v[0]["max(priority)"] + 1
		else:
			return 0
	def AddToPlaylist(self, playlist_id, song_id):
		priority = self.NextPlaylistSong(playlist_id)
		c = self.conn.cursor()
		c.execute("INSERT INTO playlist_contents (playlist_id, song_id, priority) VALUES (?, ?, ?)", [playlist_id, song_id, priority])
		self.conn.commit()
	def RemoveFromPlaylist(self, playlist_id, song_id):
		c = self.conn.cursor()
		c.execute("DELETE FROM playlist_contents WHERE playlist_id = ? AND song_id = ?", [playlist_id, song_id])
		self.conn.commit()
	def CreatePlaylist(self, user, title):
		c = self.conn.cursor()
		c.execute("INSERT INTO playlists (who, title) VALUES (?, ?)", [user, title])
		self.conn.commit()
	def DeletePlaylist(self, playlist_id):
		c = self.conn.cursor()
		c.execute("DELETE FROM playlists WHERE playlist_id = ?", [playlist_id])
		c.execute("DELETE FROM playlist_contents WHERE playlist_id = ?", [playlist_id])
		self.conn.commit()
	def Purge(self, user, player_id):
		c = self.conn.cursor()
		c.execute("DELETE FROM votes WHERE player_id = ? AND who = ?", [player_id, user])
		self.conn.commit()
	def DeletePlayer(self, player_id):
		c = self.conn.cursor()
		c.execute("DELETE FROM players WHERE player_id = ?", [player_id])
		self.conn.commit()
	def CreatePlayer(self, player_id, local_id, volume):
		c = self.conn.cursor()
		c.execute("INSERT INTO players (player_id, local_id, volume) VALUES (?, ?, ?)", [player_id, local_id, volume])
		self.conn.commit()
	def UpdatePlayer(self, player_id, args):
		c = self.conn.cursor()
		a = []
		s = []
		for k,v in args.items():
			s.append("%s = ? " % k)
			a.append(v)
		s = ", ".join(s)
		a.append(player_id)
		c.execute("UPDATE players SET %s WHERE player_id = ?" % s, a)
		self.conn.commit()
	def UpdateSong(self, song_id, args):
		c = self.conn.cursor()
		valid = ["path", "artist", "albumartist", "album", "title", "disc", "length", "track"]
		a = []
		s = []
		for k,v in args.items():
			if k in valid:
				s.append("%s = ? " % k)
				a.append(v)
		s = ", ".join(s)
		a.append(song_id)
		c.execute("UPDATE songs SET %s WHERE song_id = ?" % s, a)
		self.conn.commit()
	def AddSong(self, args):
		c = self.conn.cursor()
		valid = ["path", "artist", "albumartist", "album", "title", "disc", "length", "track"]
		keys   = []
		qms    = []
		values = []
		keys.append("online")
		qms.append("?")
		values.append(1)
		for k,v in args.items():
			if k in valid:
				keys.append(k)
				qms.append("?")
				values.append(v)
		keys = ", ".join(keys)
		qms  = ", ".join(qms)
		c.execute("INSERT INTO songs (%s) VALUES (%s)" % (keys, qms), values)
		self.conn.commit()
	def NextSong(self, player_id):
		x = self.PlayerQueue(player_id)
		if x:
			return x[0]
		else:
			return self.Random(limit=1)[0]
	def PlayerQueue(self, player):
		# TODO: Actual queuing
		raw = self.SongsByVotes(player)
		outlist = []
		output  = {}
		x = self.SELECT("players", {"player_id": player})
		for i in raw:
			if x and x[0]['song_id'] == i['song_id']: continue
			outlist.append(i)

		votes = outlist[:]

		debt = {}
		who  = []

		for i in outlist:
			if not i['who'] in who:
				who.append(i['who'])

		for i in who:
			if not i in debt:
				debt[i] = 0

		def getOrderedVotes(w):
			out = []
			x = 0
			# Slow sort, because fuck it
			for i in outlist:
				if w == i["who"]:
					out.append(i)
			return sorted(out, key = lambda song: song["priority"])

		def sorter(w):
			if next_songs[w]:
				return debt[w] * 10000 + next_songs[w][0]["length"]
			else:
				return 10000000000

		def getBestChoices(next_songs):
			return sorted(who, key=sorter)

		def _remove(outlist, nextsong):
			newoutlist = []
			for i in outlist:
				if i["song_id"] != nextsong['song_id']:
					newoutlist.append(i)
			return newoutlist

		playlist = []

		while outlist:
			next_songs = {}
			for w in who:
				next_songs[w] = getOrderedVotes(w)
			best_choices = getBestChoices(next_songs)
			nextsong = next_songs[best_choices[0]][0]
			outlist = _remove(outlist, nextsong)
			playlist.append(nextsong)
			remaining_voters = who[:]
			voters = []
			for i in votes:
				if i['song_id'] == nextsong['song_id']:
					if i['who'] in remaining_voters:
						remaining_voters.remove(i['who'])
					if i['who'] not in voters:
						voters.append(i['who'])
			payout = (float(nextsong['length']) + 1.0) / (float(len(remaining_voters)) + 1.0)
			for i in remaining_voters:
				debt[i] -= payout
			for i in voters:
				debt[i] += payout

		final_output = []
		for i in playlist:
			x = self.SELECT("votes", {"song_id": i["song_id"], "player_id": player})
			i['who'] = []
			for j in x:
				i['who'].append(j['who'])
			final_output.append(i)
		return final_output
	def UpdateVote(self, song_id, who, player, priority):
		c = self.conn.cursor()
		c.execute("UPDATE votes SET priority = ? WHERE song_id = ? AND who = ? AND player_id = ?", [priority, song_id, who, player])
		self.conn.commit()

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
	def AddVote(self, user, player, song, priority):
		c = self.conn.cursor()
		c.execute("INSERT INTO votes (song_id, time, player_id, who, priority) VALUES (?, date('now'), ?, ?, ?)", [song, player, user, priority])
		self.conn.commit()
	def do(self, statement):
		c = self.conn.cursor()
		c.execute(statement)
		self.conn.commit()
