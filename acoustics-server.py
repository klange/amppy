#!/usr/bin/env python3

import http.server, http.cookies
import socketserver, base64, subprocess
import os, json, sys, time, uuid, tempfile, importlib
from urllib.parse import urlparse, parse_qs

sys.path.append('lib')
from amp import db, config
import amp.players
import amp.rpc.local

PORT = 6969

mode_registry = {}


class ModeMeta(type):
	def __new__(cls, name, bases, dct):
		new_cls = super(ModeMeta, cls).__new__(cls, name, bases, dct)
		if 'name' in dct:
			mode_registry[dct['name']] = new_cls
		if 'names' in dct:
			for name in dct['names']:
				mode_registry[name] = new_cls
		return new_cls


class Mode(metaclass=ModeMeta):
	def __init__(self, server, session):
		self.owner = server
		self.session = session

	def get(self, args):
		return (400, {"api_error": "Internal API error: You have requested a mode which was initialized by not implemented by the server."})


class ModeStatus(Mode):
	name = "status"

	def get(self, args):
		output = {}
		output["selected_player"] = self.session._player
		output["players"] = self.owner.players
		output["player"] = self.session.player()
		output["now_playing"] = self.session.currentSong()
		output["playlist"] = self.owner.db.PlayerQueue(self.session._player)
		output["who"] = self.session.user()
		output["can_skip"] = self.session.can_skip()
		output["is_admin"] = self.session.is_admin()
		return (200, output)


class ModeGlobalStatus(Mode):
	name = "global_status"

	def get(self, args):
		output = {}
		output["who"] = self.session.user()
		output["player_names"] = self.owner.players
		output["players"] = {}
		for i in output['player_names']:
			x = self.owner.db.SELECT("players", {"player_id": i})
			if x:
				pl = {}
				pl["info"] = x[0]
				pl["song"] = self.owner.db.SELECT("songs", {"song_id": x[0]["song_id"]})[0]
				output["players"][i] = pl
		return (200, output)


class ModeSearch(Mode):
	name = "paged_search"

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
	name = "quick_search"

	def get(self, args):
		if "q" not in args:
			return (400, {"api_error": "Quick search results a 'q' argument."})
		limit = 10
		if "limit" in args: limit = args["limit"]
		results = self.owner.db.QuickSearch(args["q"], limit)
		return (200, results)


class ModeRandom(Mode):
	name = "random"

	def get(self, args):
		limit = 10
		if "amount" in args: limit = args["amount"]
		results = self.owner.db.Random(limit)
		return (200, results)


class ModeRecent(Mode):
	name = "recent"

	def get(self, args):
		limit = 10
		if "amount" in args: limit = args["amount"]
		results = self.owner.db.Recent(limit)
		return (200, results)


class ModeHistory(Mode):
	name = "history"

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
	name = "get_details"

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
	name = "art"

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
		path = "web/www-data/icons/cd_case.png"
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

class ModeReorderQueue(Mode):
	name = "reorder_queue"

	def get(self, args):
		if not self.session.user():
			return (500, {"auth_error": "You must login to vote for songs."})
		if "song_id" not in args:
			return ModeStatus.get(self, [])
		p = 0
		for i in args["song_id"].split(";"):
			self.owner.db.UpdateVote(i, self.session.user(), self.session._player, p)
			p += 1

		return ModeStatus.get(self, [])




class ModeSelect(Mode):
	name = "select"

	def get(self, args):
		if "field" not in args:
			return (400, {"api_error": "select requires a 'field' argument."})
		if "value" not in args:
			return (400, {"api_error": "select requires a 'value' argument."})
		return (200, self.owner.db.Select(args["field"], args["value"]))


class ModeChangePlayer(Mode):
	name = "change_player"

	def get(self, args):
		if "player_id" not in args:
			return (400, {"api_error": "Player change requires a player to change to."})
		if args["player_id"] not in self.owner.players:
			return (400, {"api_error": "Bad player id."})
		self.session._player = args["player_id"]
		return ModeStatus.get(self, args)


class ModeTopVoted(Mode):
	name = "top_voted"

	def get(self, args):
		if "limit" in args:
			limit = args["limit"]
		else:
			limit = 10
		return (200, self.owner.db.TopVoted(limit))


class ModeAlbumSearch(Mode):
	name = "album_search"

	def get(self, args):
		if "album" not in args:
			return (400, {"api_error": "album_search requires an 'album' argument."})
		return (200, self.owner.db.AlbumSearch(args["album"]))


class ModeVote(Mode):
	name = "vote"

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
	name = "unvote"

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
	name = "playlists"

	def get(self, args):
		who = ""
		title = ""
		if "who" in args: who = args["who"]
		if "title" in args: title = args["title"]
		return (200, self.owner.db.Playlists(who,title))


class ModePlaylistsLoose(Mode):
	name = "playlists_loose"

	def get(self, args):
		value = ""
		if "value" in args: value = args["value"]
		return (200, self.owner.db.PlaylistsLoose(value))


class ModePlaylistContents(Mode):
	name = "playlist_contents"

	def get(self, args):
		if not "playlist_id" in args:
			return (400, {"api_error": "playlist_contents requires a 'playlist_id' argument."})
		return (200, self.owner.db.PlaylistContents(args["playlist_id"]))


class ModePlaylistInfo(Mode):
	name = "playlist_info"

	def get(self, args):
		if not "playlist_id" in args:
			return (400, {"api_error": "playlist_info requires a 'playlist_id' argument."})
		return (200, self.owner.db.PlaylistInfo(args["playlist_id"]))


class ModeAddToPlaylist(Mode):
	name = "add_to_playlist"

	def get(self, args):
		if not self.session.user():
			return (500, {"auth_error": "You must login to modify playlists."})
		if "song_id" not in args:
			return (400, {"api_error": "add_to_playlist requires a 'song_id' argument."})
		if not "playlist_id" in args:
			return (400, {"api_error": "add_to_playlist requires a 'playlist_id' argument."})
		(discard, playlist) = ModePlaylistInfo.get(self, args)
		if playlist['who'] != self.session.user() and not self.session.is_admin():
			return (500, {"auth_error": "You are not permitted to modify this playlist."})
		if ";" in args["song_id"]:
			for i in args["song_id"].split(";"):
				self.owner.db.AddToPlaylist(args["playlist_id"], i)
		else:
			self.owner.db.AddToPlaylist(args["playlist_id"], args['song_id'])
		return ModePlaylistContents.get(self, args)


class ModeRemoveFromPlaylist(Mode):
	name = "remove_from_playlist"
	def get(self, args):
		if not self.session.user():
			return (500, {"auth_error": "You must login to modify playlists."})
		if "song_id" not in args:
			return (400, {"api_error": "remove_from_playlist requires a 'song_id' argument."})
		if not "playlist_id" in args:
			return (400, {"api_error": "remove_from_playlist requires a 'playlist_id' argument."})
		(discard, playlist) = ModePlaylistInfo.get(self, args)
		if playlist['who'] != self.session.user() and not self.session.is_admin():
			return (500, {"auth_error": "You are not permitted to modify this playlist."})
		if ";" in args["song_id"]:
			for i in args["song_id"].split(";"):
				self.owner.db.RemoveFromPlaylist(args["playlist_id"], i)
		else:
			self.owner.db.RemoveFromPlaylist(args["playlist_id"], args['song_id'])
		return ModePlaylistContents.get(self, args)


class ModeCreatePlaylist(Mode):
	name = "create_playlist"

	def get(self, args):
		if not self.session.user():
			return (500, {"auth_error": "You must login to modify playlists."})
		if not "title" in args:
			return (400, {"api_error": "create_playlist requires a 'title' argument."})
		self.owner.db.CreatePlaylist(self.session.user(), args["title"])
		args["who"] = self.session.user()
		return ModePlaylists.get(self, args)


class ModeDeletePlaylist(Mode):
	name = "delete_playlist"

	def get(self, args):
		if not self.session.user():
			return (500, {"auth_error": "You must login to modify playlists."})
		if not "playlist_id" in args:
			return (400, {"api_error": "delete_playlist requires a 'playlist_id' argument."})
		(discard, playlist) = ModePlaylistInfo.get(self, args)
		if playlist['who'] != self.session.user() and not self.session.is_admin():
			return (500, {"auth_error": "You are not permitted to modify this playlist."})
		self.owner.db.DeletePlaylist(args["playlist_id"])
		args["who"] = self.session.user()
		return ModePlaylists.get(self, args)


class ModePurge(Mode):
	name = "purge"

	def get(self, args):
		if not self.session.user():
			return (500, {"auth_error": "This action can only be executed by logged-in uesrs."})
		if not "who" in args or not self.session.is_admin():
			args["who"] = self.session.user()
		self.owner.db.Purge(args["who"], self.session._player)
		return ModeStatus.get(self, args)


class ModeStats(Mode):
	name = "stats"

	def get(self, args):
		who = None
		if "who" in args: who = args["who"]
		output = {}
		output["total_songs"] = self.owner.db.SongCount()
		output["top_artists"] = self.owner.db.TopArtists(who)
		return (200, output)


class ModeControls(Mode):
	names = ["start", "stop", "skip", "pause", "volume", "zap"]

	def get(self, args):
		if not self.session.user():
			return (500, {"auth_error": "You must login to control the player."})
		_args = [args["mode"]]
		if "value" in args:
			_args.append(args["value"])
		if args["mode"] == "skip" and not self.session.can_skip():
				return (500, {"auth_error": "You can not skip this song."})
		self.owner.rpc(self.session._player, _args)
		time.sleep(1) # Give the players a bit of time to update the DB
		return ModeStatus.get(self, [])

class ModeSessions(Mode):
	name = "sessions"

	def get(self, args):
		if not self.session.is_admin():
			return (500, {"auth_error": "You are not permitted to view this information."})
		sessions = {}
		for k,v in self.owner.sessions.items():
			sessions[k] = {}
			sessions[k]['is_admin'] = v.is_admin()
			sessions[k]['user'] = v.user()
			sessions[k]['player'] = v._player
			sessions[k]['created'] = v.created
			sessions[k]['address'] = v.remote
		return (200, sessions)


class AcousticsSession(object):
	def __init__(self, sessid, owner, remote_host):
		self.owner   = owner
		self.sessid  = sessid
		self._user   = None
		self._player = self.owner.players[0]
		self.created = int(time.time())
		self.remote  = remote_host
	def is_admin(self):
		return not (self._user is None)
	def can_skip(self):
		return not (self._user is None)
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
		self.modes = mode_registry
		self.config = config.AcousticsConfig()
		self.db = db.Sqlite(self.config["database"]["data_source"].split(":")[-1])
		self.sessions = {}
		self.players = self.config["{}"]['players'].split(",")
	def newSession(self, client_address):
		sid = str(uuid.uuid1())
		self.sessions[sid] = AcousticsSession(sid, self, client_address)
		return sid

	def rpc(self, player_id, args):
		if player_id in self.players:
			rpc_module = importlib.import_module(self.config.translate(self.config['player.'+player_id]["rpc"]))
			player = rpc_module.RPC()
			player.execute(player_id, args)

	def execute(self, session, args):
		if args["mode"] in self.modes:
			return self.modes[args["mode"]](self, self.sessions[session]).get(args)
		else:
			return (400, {"api_error": "Unrecognized mode `%s`" % args["mode"]})

def AcousticsHandlerFactory(server):
	failures = {}
	handler = AcousticsHandler
	handler.acoustics_server = server
	handler.failures = failures
	return handler

class AcousticsHandler(http.server.SimpleHTTPRequestHandler):
	def do_GET(self):
		if 'cookie' in self.headers:
			self.cookie = http.cookies.SimpleCookie(self.headers["cookie"])
		else:
			self.cookie = http.cookies.SimpleCookie()
		session = None
		if "sessid" in self.cookie and self.cookie['sessid'].value in self.acoustics_server.sessions:
			session = self.cookie["sessid"].value
		else:
			if "sessid" in self.cookie:
				print("Bad session from previous instance?", self.cookie["sessid"].value)
			if self.client_address[0] not in self.failures.keys():
				print("First time, trying to give out session key for " + self.client_address[0])
				self.failures[self.client_address[0]] = 0
			self.failures[self.client_address[0]] += 1
			session = self.acoustics_server.newSession(self.client_address)
			self.cookie["sessid"] = session
			print("serving fresh session", session)
			if self.failures[self.client_address[0]] > 5:
				print("Failed too many times, going to have to duck out.")
				self.failures[self.client_address[0]] -= 5
				self.send_response(400)
				self.send_header('Content-type', 'text/html')
				self.send_header('Set-Cookie', self.cookie.output(header="").strip())
				self.end_headers()
				self.wfile.write(b"Your browser is not accepting a required session cookie, please try refreshing.")
				return
			else:
				self.send_response(307)
				self.send_header('Location', self.path)
				self.send_header('Set-Cookie', self.cookie['sessid'].output(header="").strip())
				self.end_headers()
				return
		if self.path.startswith("/www-data/auth"):
			# Replace this with your own authorization as necessary.
			if 'Authorization' in self.headers:
				if self.headers["Authorization"].startswith('Basic '):
					tmp = base64.standard_b64decode(bytes(self.headers['Authorization'].split(" ")[1].encode('utf-8'))).decode("utf-8")
					# TODO: Actual authentication
					self.acoustics_server.sessions[session]._user = tmp.split(":")[0]
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
			result = self.acoustics_server.execute(session, args)
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
			self.path = os.path.join("web", self.path.replace("/","",1))
			if not os.path.realpath(self.path).startswith(os.path.realpath("web")):
				self.send_response(400)
				self.end_headers()
				return
			return http.server.SimpleHTTPRequestHandler.do_GET(self)

class AcousticsSocket(socketserver.TCPServer):
	allow_reuse_address = True

if __name__ == "__main__":
	server = AcousticsServer()
	httpd = AcousticsSocket(("", PORT), AcousticsHandlerFactory(server))
	httpd.serve_forever()
