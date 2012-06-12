#!/usr/bin/env python3

import http.server, http.cookies
import socketserver, base64
import os, json, sys, time, uuid
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
		output["can_skip"] = True
		output["is_admin"] = True
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
		obj = self.owner.db.SELECT("songs", {"song_id": args["song_id"]})[0]
		print(obj["path"])
		possible = ["acoustics-art.png", "acoustics-art.jpg", "cover.png", "cover.jpg", "Folder.png", "Folder.jpg"]
		for i in possible:
			fpath = os.path.join(os.path.dirname(obj["path"]),i)
			if os.path.exists(fpath):
				print("Found: %s" % fpath)
		return (200, b"lolbuts", "text/html")


class ModeChangePlayer(Mode):
	def get(self, args):
		if "player_id" not in args:
			return (400, {"api_error", "Player change requires a player to change to."})
		if args["player_id"] not in self.owner.getPlayers():
			return (400, {"api_error", "Bad player id."})
		self.session._player = args["player_id"]
		return ModeStatus.get(self, args)

class AcousticsSession(object):
	def __init__(self, sessid, owner):
		self.owner   = owner
		self.sessid  = sessid
		self._user   = None
		self._player = self.owner.getPlayers()[0]
		self.created = int(time.time())
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

class AcousticsHandler(http.server.SimpleHTTPRequestHandler):
	def do_GET(self):
		global server
		if 'cookie' in self.headers:
			self.cookie = http.cookies.SimpleCookie(self.headers["cookie"])
		else:
			self.cookie = http.cookies.SimpleCookie()
		session = None
		if "sessid" in self.cookie and self.cookie['sessid'].value in server.sessions:
			session = self.cookie["sessid"].value
		else:
			session = server.newSession()
			self.cookie["sessid"] = session
			self.send_response(307)
			self.send_header('Location', self.path)
			self.send_header('Cookie', self.cookie)
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
