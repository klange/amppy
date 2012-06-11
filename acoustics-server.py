#!/usr/bin/env python3

import http.server
import socketserver
import os, json, sys, time
from urllib.parse import urlparse, parse_qs

sys.path.append('lib')
from amp import db

PORT = 6969

class Mode(object):
	def __init__(self, server):
		self.owner = server
		pass
	def get(self, args):
		return (400, {"api_error": "Internal API error: You have requested a mode which was initialized by not implemented by the server."})

class ModeStatus(Mode):
	def get(self, args):
		output = {}
		output["selected_player"] = "default"
		output["players"] = ["default"]
		output["player"] = self.owner.player()
		output["now_playing"] = self.owner.currentSong()
		output["playlist"] = []
		output["who"] = "..."
		output["can_skip"] = True
		output["is_admin"] = True
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

class AcousticsServer(object):
	def __init__(self):
		self.modes = {}
		self.db = db.Sqlite('/home/klange/Music/amp.sqlite')
	def player(self):
		x = self.db.SELECT("players", {"player_id": "default"})
		if x:
			return x[0]
		else:
			return None
	def currentSong(self):
		if not self.player():
			return None
		obj = self.db.SELECT("songs", {"song_id": self.player()["song_id"]})[0]
		obj["now"] = int(time.time())
		obj["who"] = []
		return obj
	def execute(self, args):
		if args["mode"] in self.modes:
			return self.modes[args["mode"]].get(args)
		else:
			return (400, {"api_error": "Unrecognized mode `%s`" % args["mode"]})

server = AcousticsServer()
server.modes["status"] = ModeStatus(server)
server.modes["paged_search"] = ModeSearch(server)
server.modes["quick_search"] = ModeQuickSearch(server)
server.modes["random"] = ModeRandom(server)
server.modes["history"] = ModeHistory(server)
server.modes["recent"] = ModeRecent(server)

class AcousticsHandler(http.server.SimpleHTTPRequestHandler):
	def do_GET(self):
		global server
		if self.path.startswith("/json."):
			# Parse API call
			path = urlparse(self.path)
			args = parse_qs(path.query,keep_blank_values=True)
			for k in args.keys():
				args[k] = ";".join(args[k])
			if "mode" not in args:
				args["mode"] = "status"
			(status, results) = server.execute(args)
			# Respond appropriately
			self.send_response(status)
			self.send_header('Content-type', 'application/json')
			self.end_headers()
			self.wfile.write(json.dumps(results).encode("utf-8"))
		else:
			return http.server.SimpleHTTPRequestHandler.do_GET(self)

class AcousticsSocket(socketserver.TCPServer):
	allow_reuse_address = True

if __name__ == "__main__":
	os.chdir("web")
	httpd = AcousticsSocket(("",6969), AcousticsHandler)
	httpd.serve_forever()
