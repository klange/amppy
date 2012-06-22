import configparser, os

class AcousticsConfig(configparser.ConfigParser):
	def __init__(self):
		config_string = open(os.path.join(os.path.dirname(__file__), "../../conf/acoustics.ini"), 'r').read()
		configparser.ConfigParser.__init__(self)
		self.read_string("[{}]\n" + config_string)
	def translate(self, module):
		return module.replace("Acoustics::", "amp.").replace("::",".").lower()

