#!/usr/bin/env python3
import sys
import unittest

sys.path.append('lib')
import amp.config

class TestConfig(unittest.TestCase):
	def setUp(self):
		self.config = amp.config.AcousticsConfig(config_string="""
players=default,extra
webroot=/amp/
[database]
data_source=/home/klange/Music/amp.sqlite

[scanner]
require_prefix=

[player.default]
name=default
module=Acoustics::Player::MPlayer
rpc=Acoustics::RPC::Local
queue=TimeSlice
default_volume = 70
extensions=LastFM::Scrobbler

[player.extra]
name=extra
module=Acoustics::Player::MPlayer
rpc=Acoustics::RPC::Local
queue=TimeSlice
default_volume=70

[webauth]
module=Acoustics::Web::Auth::Simple
field=REMOTE_ADDR
"""
		)

	def test_database(self):
		self.assertEqual(self.config.database_uri, '/home/klange/Music/amp.sqlite')

	def test_players_configured(self):
		self.assertEqual(list(sorted(self.config.players.keys())), ['default', 'extra'])

	def test_players_default_name(self):
		self.assertEqual(self.config.players['default'].name, 'default')

	def test_players_default_module(self):
		self.assertEqual(self.config.players['default'].module_name, 'amp.rpc.local.RPC')

if __name__ == '__main__':
	unittest.main()
