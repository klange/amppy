#!/usr/bin/env python3

import http.server, http.cookies
import socketserver, base64, subprocess
import os, json, sys, time, uuid, tempfile
from urllib.parse import urlparse, parse_qs

sys.path.append('lib')
from amp import db

PORT = 6969

class Mode(object):
	def __init__(self, server, session):
		self.owner = server
		self.session = session
		pass
	def get(self, args):
		return (400, {"api_error": "Internal API error: You have requested a mode which was initialized by not implemented by the server."})

class ModeStatus(Mode):
	def get(self, args):
		output = {}
		output["selected_player"] = self.session._player
		output["players"] = self.owner.getPlayers()
		output["player"] = self.session.player()
		output["now_playing"] = self.session.currentSong()
		output["playlist"] = self.owner.getQueue(self.session._player)
		output["who"] = self.session.user()
		output["can_skip"] = self.session.can_skip()
		output["is_admin"] = self.session.is_admin()
		return (200, output)

class ModeGlobalStatus(Mode):
	def get(self, args):
		output = {}
		output["who"] = self.session.user()
		output["player_names"] = self.owner.getPlayers()
		output["players"] = []
		for i in output['player_names']:
			x = self.owner.db.SELECT("players", {"player_id": i})
			if x: output["players"].append(x)
		return (200, output)

class ModeSearch(Mode):
	def get(self, args):
		if "value" not in args:
			return (400, {"api_error": "Search requests require a 'value' argument."})
		limit = 10
		offset = 0
		if "limit" in args: limit = args["limit"]
		if "offset" in args: offset = args["offset"]
		results = self.owner.db.Search(args["value"], limit, offset)
		return (200, results)

class ModeQuickSearch(Mode):
	def get(self, args):
		if "q" not in args:
			return (400, {"api_error": "Quick search results a 'q' argument."})
		limit = 10
		if "limit" in args: limit = args["limit"]
		results = self.owner.db.QuickSearch(args["q"], limit)
		return (200, results)

class ModeRandom(Mode):
	def get(self, args):
		limit = 10
		if "amount" in args: limit = args["amount"]
		results = self.owner.db.Random(limit)
		return (200, results)

class ModeRecent(Mode):
	def get(self, args):
		limit = 10
		if "amount" in args: limit = args["amount"]
		results = self.owner.db.Recent(limit)
		return (200, results)

class ModeHistory(Mode):
	def get(self, args):
		limit = 10
		voter = None
		if "amount" in args: limit = args["amount"]
		if "voter" in args: voter = args["voter"]
		results = self.owner.db.History(voter=voter, limit=limit)
		history = []
		for song in results:
			if len(history) and song["song_id"] == history[-1]["song_id"] and history[-1]["time"] == song["time"]:
				history[-1]["who"].append(song["who"])
			else:
				song["who"] = [song["who"]]
				history.append(song)
		return (200, results)

class ModeDetails(Mode):
	def get(self, args):
		if "song_id" not in args:
			return (400, {"api_error": "get_details requires a 'song_id'"})
		obj = self.owner.db.SELECT("songs", {"song_id": args["song_id"]})[0]
		obj["now"] = int(time.time())
		voters = self.owner.db.SELECT("votes", {"song_id" : obj["song_id"], "player_id": self.session._player})
		obj["who"] = []
		for i in voters:
			obj["who"].append(i['who'])
		return (200, {"song": obj})

class ModeArt(Mode):
	def get(self, args):
		if "song_id" not in args:
			return (400, {"api_error": "art requires a 'song_id'"})
		if "size" not in args:
			size = 500
		else:
			size = int(args["size"])
		if size > 1000:
			size = 1000
		obj = self.owner.db.SELECT("songs", {"song_id": args["song_id"]})[0]
		possible = ["acoustics-art.png", "acoustics-art.jpg", "cover.png", "cover.jpg", "Folder.png", "Folder.jpg"]
		path = "www-data/icons/cd_case.png"
		for i in possible:
			fpath = os.path.join(os.path.dirname(obj["path"]),i)
			if os.path.exists(fpath):
				path = fpath
				break
		f = tempfile.NamedTemporaryFile()
		subprocess.call(["convert", path, "-resize", "%dx%d" % (size,size), f.name])
		filecontents = f.read()
		f.close()
		return (200, filecontents, "image/png")

class ModeSelect(Mode):
	def get(self, args):
		if "field" not in args:
			return (400, {"api_error": "select requires a 'field' argument."})
		if "value" not in args:
			return (400, {"api_error": "select requires a 'value' argument."})
		return (200, self.owner.db.Select(args["field"], args["value"]))


class ModeChangePlayer(Mode):
	def get(self, args):
		if "player_id" not in args:
			return (400, {"api_error", "Player change requires a player to change to."})
		if args["player_id"] not in self.owner.getPlayers():
			return (400, {"api_error", "Bad player id."})
		self.session._player = args["player_id"]
		return ModeStatus.get(self, args)

class ModeTopVoted(Mode):
	def get(self, args):
		if "limit" in args:
			limit = args["limit"]
		else:
			limit = 10
		return (200, self.owner.db.TopVoted(limit))

class ModeAlbumSearch(Mode):
	def get(self, args):
		if "album" not in args:
			return (400, {"api_error": "album_search requires an 'album' argument."})
		return (200, self.owner.db.AlbumSearch(args["album"]))

class ModeVote(Mode):
	def get(self, args):
		if not self.session.user():
			return (500, {"auth_error": "You must login to vote for songs."})
		if "song_id" not in args:
			return (400, {"api_error": "vote requires a 'song_id' argument."})
		priorityNumber = self.owner.db.NextVote(self.session.user(), self.session._player)
		# XXX: We don't check max-votes
		if ";" in args["song_id"]:
			for i in args["song_id"].split(";"):
				self.owner.db.AddVote(self.session.user(), self.session._player, i, priorityNumber)
		else:
			self.owner.db.AddVote(self.session.user(), self.session._player, args['song_id'], priorityNumber)
		return ModeStatus.get(self, args)

class ModeUnvote(Mode):
	def get(self, args):
		if not self.session.user():
			return (500, {"auth_error": "You must login to vote for songs."})
		if "song_id" not in args:
			return (400, {"api_error": "vote requires a 'song_id' argument."})
		if ";" in args["song_id"]:
			for i in args["song_id"].split(";"):
				self.owner.db.Unvote(self.session.user(), i)
		else:
			self.owner.db.Unvote(self.session.user(), args['song_id'])
		return ModeStatus.get(self, args)

class ModePlaylists(Mode):
	def get(self, args):
		who = ""
		title = ""
		if "who" in args: who = args["who"]
		if "title" in args: title = args["title"]
		return (200, self.owner.db.Playlists(who,title))

class ModePlaylistsLoose(Mode):
	def get(self, args):
		value = ""
		if "value" in args: value = args["value"]
		return (200, self.owner.db.PlaylistsLoose(value))

class ModePlaylistContents(Mode):
	def get(self, args):
		if not "playlist_id" in args:
			return (400, {"api_error": "playlist_contents requires a 'playlist_id' argument."})
		return (200, self.owner.db.PlaylistContents(args["playlist_id"]))

class ModePlaylistInfo(Mode):
	def get(self, args):
		if not "playlist_id" in args:
			return (400, {"api_error": "playlist_info requires a 'playlist_id' argument."})
		return (200, self.owner.db.PlaylistInfo(args["playlist_id"]))

class ModeAddToPlaylist(Mode):
	def get(self, args):
		if not self.session.user():
			return (500, {"auth_error": "You must login to modify playlists."})
		if "song_id" not in args:
			return (400, {"api_error": "add_to_playlist requires a 'song_id' argument."})
		if not "playlist_id" in args:
			return (400, {"api_error", "add_to_playlist requires a 'playlist_id' argument."})
		(discard, playlist) = ModePlaylistInfo.get(self, args)
		if playlist['who'] != self.session.user() and not self.session.is_admin():
			return (500, {"auth_error", "You are not permitted to modify this playlist."})
		if ";" in args["song_id"]:
			for i in args["song_id"].split(";"):
				self.owner.db.AddToPlaylist(args["playlist_id"], i)
		else:
			self.owner.db.AddToPlaylist(args["playlist_id"], args['song_id'])
		return ModePlaylistContents.get(self, args)

class ModeRemoveFromPlaylist(Mode):
	def get(self, args):
		if not self.session.user():
			return (500, {"auth_error": "You must login to modify playlists."})
		if "song_id" not in args:
			return (400, {"api_error": "remove_from_playlist requires a 'song_id' argument."})
		if not "playlist_id" in args:
			return (400, {"api_error", "remove_from_playlist requires a 'playlist_id' argument."})
		(discard, playlist) = ModePlaylistInfo.get(self, args)
		if playlist['who'] != self.session.user() and not self.session.is_admin():
			return (500, {"auth_error", "You are not permitted to modify this playlist."})
		if ";" in args["song_id"]:
			for i in args["song_id"].split(";"):
				self.owner.db.RemoveFromPlaylist(args["playlist_id"], i)
		else:
			self.owner.db.RemoveFromPlaylist(args["playlist_id"], args['song_id'])
		return ModePlaylistContents.get(self, args)

class ModeCreatePlaylist(Mode):
	def get(self, args):
		if not self.session.user():
			return (500, {"auth_error": "You must login to modify playlists."})
		if not "title" in args:
			return (400, {"api_error", "create_playlist requires a 'title' argument."})
		self.owner.db.CreatePlaylist(self.session.user(), args["title"])
		args["who"] = self.session.user()
		return ModePlaylists.get(self, args)

class ModeDeletePlaylist(Mode):
	def get(self, args):
		if not self.session.user():
			return (500, {"auth_error": "You must login to modify playlists."})
		if not "playlist_id" in args:
			return (400, {"api_error", "delete_playlist requires a 'playlist_id' argument."})
		(discard, playlist) = ModePlaylistInfo.get(self, args)
		if playlist['who'] != self.session.user() and not self.session.is_admin():
			return (500, {"auth_error", "You are not permitted to modify this playlist."})
		self.owner.db.DeletePlaylist(args["playlist_id"])
		args["who"] = self.session.user()
		return ModePlaylists.get(self, args)

class ModePurge(Mode):
	def get(self, args):
		if not self.session.user():
			return (500, {"auth_error": "This action can only be executed by logged-in uesrs."})
		if not "who" in args or not self.session.is_admin():
			args["who"] = self.session.user()
		self.owner.db.Purge(args["who"], self.session._player)
		return ModeStatus.get(self, args)


class ModeStats(Mode):
	def get(self, args):
		who = None
		if "who" in args: who = args["who"]
		output = {}
		output["total_songs"] = self.owner.db.SongCount()
		output["top_artists"] = self.owner.db.TopArtists(who)
		return (200, output)

class AcousticsSession(object):
	def __init__(self, sessid, owner):
		self.owner   = owner
		self.sessid  = sessid
		self._user   = None
		self._player = self.owner.getPlayers()[0]
		self.created = int(time.time())
	def is_admin(self):
		return True
	def can_skip(self):
		# Should be current_song->who = me || current_song->who = None
		return True
	def user(self):
		return self._user
	def player(self):
		x = self.owner.db.SELECT("players", {"player_id": self._player})
		if x:
			return x[0]
		else:
			return None
	def currentSong(self):
		if not self.player():
			return None
		obj = self.owner.db.SELECT("songs", {"song_id": self.player()["song_id"]})[0]
		obj["now"] = int(time.time())
		voters = self.owner.db.SELECT("votes", {"song_id" : obj["song_id"], "player_id": self._player})
		obj["who"] = []
		for i in voters:
			obj["who"].append(i['who'])
		return obj

class AcousticsServer(object):
	def __init__(self):
		self.modes = {}
		self.db = db.Sqlite('/home/klange/Music/amp.sqlite')
		self.sessions = {}
	def getQueue(self, player):
		# TODO: Actual queuing
		raw = self.db.SongsByVotes(player)
		outlist = []
		output  = {}
		x = self.db.SELECT("players", {"player_id": player})
		for i in raw:
			if x and x[0]['song_id'] == i['song_id']: continue
			if i["song_id"] in output:
				output[i["song_id"]]["priority"][i["who"]] = i["priority"]
				output[i["song_id"]]["who"].append(i["who"])
			else:
				i["priority"] = {i["who"]: i["priority"]}
				i["who"] = [i["who"]]
				output[i["song_id"]] = i
				outlist.append(i)
		return outlist
	def addMode(self, name, mode_type):
		self.modes[name] = mode_type
	def getPlayers(self):
		# TODO: Read from configuration file [python?]
		return ["default", "extra"]
	def newSession(self):
		sid = str(uuid.uuid1())
		self.sessions[sid] = AcousticsSession(sid, self)
		return sid
	def execute(self, session, args):
		if args["mode"] in self.modes:
			return self.modes[args["mode"]](server, self.sessions[session]).get(args)
		else:
			return (400, {"api_error": "Unrecognized mode `%s`" % args["mode"]})

server = AcousticsServer()
server.addMode("status", ModeStatus)
server.addMode("global_status", ModeGlobalStatus)
server.addMode("paged_search", ModeSearch)
server.addMode("quick_search", ModeQuickSearch)
server.addMode("random", ModeRandom)
server.addMode("history", ModeHistory)
server.addMode("recent", ModeRecent)
server.addMode("change_player", ModeChangePlayer)
server.addMode("get_details", ModeDetails)
server.addMode("art", ModeArt)
server.addMode("top_voted", ModeTopVoted)
server.addMode("album_search", ModeAlbumSearch)
server.addMode("select", ModeSelect)
server.addMode("vote", ModeVote)
server.addMode("unvote", ModeUnvote)
server.addMode("stats", ModeStats)
server.addMode("playlists", ModePlaylists)
server.addMode("playlists_loose", ModePlaylistsLoose)
server.addMode("playlist_contents", ModePlaylistContents)
server.addMode("playlist_info", ModePlaylistInfo)
server.addMode("add_to_playlist", ModeAddToPlaylist)
server.addMode("remove_from_playlist", ModeRemoveFromPlaylist)
server.addMode("create_playlist", ModeCreatePlaylist)
server.addMode("delete_playlist", ModeDeletePlaylist)
server.addMode("purge", ModePurge)

failures = {}

class AcousticsHandler(http.server.SimpleHTTPRequestHandler):
	def do_GET(self):
		global server, failures
		if 'cookie' in self.headers:
			self.cookie = http.cookies.SimpleCookie(self.headers["cookie"])
		else:
			self.cookie = http.cookies.SimpleCookie()
		session = None
		if "sessid" in self.cookie and self.cookie['sessid'].value in server.sessions:
			session = self.cookie["sessid"].value
		else:
			if self.client_address[0] not in failures.keys():
				print("First time, trying to give out session key for " + self.client_address[0])
				failures[self.client_address[0]] = 0
			failures[self.client_address[0]] += 1
			session = server.newSession()
			self.cookie["sessid"] = session
			if failures[self.client_address[0]] > 3:
				self.send_response(400)
				self.send_header('Content-type', 'text/html')
				self.send_header('Set-Cookie', self.cookie)
				self.end_headers()
				self.wfile.write(b"Your browser is not accepting a required session cookie, please try refreshing.")
				return
			else:
				self.send_response(307)
				self.send_header('Location', self.path)
				self.send_header('Set-Cookie', self.cookie)
				self.end_headers()
				return
		if self.path.startswith("/www-data/auth"):
			# Replace this with your own authorization as necessary.
			if 'Authorization' in self.headers:
				if self.headers["Authorization"].startswith('Basic '):
					tmp = base64.standard_b64decode(bytes(self.headers['Authorization'].split(" ")[1].encode('utf-8'))).decode("utf-8")
					# TODO: Actual authentication
					server.sessions[session]._user = tmp.split(":")[0]
					self.send_response(200)
					self.send_header('Location', '/json.pl?mode=status')
					self.end_headers()
			self.send_response(401)
			self.send_header('WWW-Authenticate', 'Basic realm="Acoustics"')
			self.end_headers()
			return
		elif self.path.startswith("/json."):
			# Parse API call
			path = urlparse(self.path)
			args = parse_qs(path.query,keep_blank_values=True)
			for k in args.keys():
				args[k] = ";".join(args[k])
			if "mode" not in args:
				args["mode"] = "status"
			result = server.execute(session, args)
			if len(result) == 2:
				(status, results) = result
				output = json.dumps(results).encode("utf-8")
				ctype = 'application/json'
			elif len(result) == 3:
				(status, output, ctype) = result
			else:
				output = "?"
				status = 400
			# Respond appropriately
			self.send_response(status)
			self.send_header('Content-type', ctype)
			self.end_headers()
			self.wfile.write(output)
		else:
			return http.server.SimpleHTTPRequestHandler.do_GET(self)

class AcousticsSocket(socketserver.TCPServer):
	allow_reuse_address = True

if __name__ == "__main__":
	os.chdir("web")
	httpd = AcousticsSocket(("",6969), AcousticsHandler)
	httpd.serve_forever()
