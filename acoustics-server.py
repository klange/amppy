#!/usr/bin/env python3

import http.server
import socketserver
import os, json
from urllib.parse import urlparse, parse_qs

PORT = 6969

class Mode(object):
	def __init__(self, server):
		self.owner = server
		pass
	def get(self, args):
		return (400, {"incomplete": 1})

class ModeStatus(Mode):
	def get(self, args):
		output = {}
		output["now_playing"] = self.owner.currentSong()
		output["selected_player"] = "default"
		output["players"] = ["default"]
		output["player"] = {}
		output["playlist"] = []
		output["who"] = "..."
		output["can_skip"] = True
		output["is_admin"] = True
		return (200, output)

class AcousticsServer(object):
	def __init__(self):
		self.modes = {}
	def currentSong(self):
		return {"track": 1,
				"path":  "/tmp/herp/derp",
				"online": 1,
				"artist": "Test",
				"album": "Album Title",
				"length": 200,
				"now": 1339379746,
				"who": [],
				"song_id": 67,
				"title": "Herp a Derp",
				"disc": None,
				"albumartist": None
				}
	def execute(self, args):
		if args["mode"] in self.modes:
			return self.modes[args["mode"]].get(args)
		else:
			return (400, {"bad_request": 400})

server = AcousticsServer()
server.modes["status"] = ModeStatus(server)

class AcousticsHandler(http.server.SimpleHTTPRequestHandler):
	def do_GET(self):
		global server
		if self.path.startswith("/json."):
			# Parse API call
			path = urlparse(self.path)
			args = parse_qs(path.query)
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
