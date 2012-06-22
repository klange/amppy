import configparser


class AcousticsPlayerConfig(object):
	def __init__(self, player_config):
		self.name = player_config['name']
		self.player_config = player_config

	@property
	def module_name(self):
		if self.player_config['module'] == 'Acoustics::RPC::Local':
			return 'amp.rpc.local.RPC'
		

class AcousticsConfig(object):
	def __init__(self, config_string=None):
		self.config = configparser.ConfigParser()
		self.config.read_string("[{}]\n" + config_string)

		# Cache of player information.
		self._players = None

	@property
	def database_uri(self):
		return self.config['database']['data_source']

	@property
	def players(self):
		if self._players is not None:
			return self._players

		player_names = self.config['{}']['players'].split(',')
		self._players = dict(
			(player_name, AcousticsPlayerConfig(self.config['player.%s' % player_name]))
			for player_name in player_names
		)
		return self._players


