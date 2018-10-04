class Dictionary:
	"""
	Dictionary Class defines a dictionary that matches:
		Command (order) as text --> URL of API to consume

	Note that in order to retrieve a functional URL, it has to be initiated beforehand by set_dictionary.
	The idea is that set_dictionary is called after resolving localization paradigm so it is known which esp32 will have
	 to act accordingly.

	"""
	__esp_ip = ""
	__esp_port = ""
	__text_to_orders = {}

	def __set_esp_ip(self, ip):
		self.__esp_ip = ip

	def __set_esp_port(self, port):
		self.__esp_port = port

	def set_dictionary(self, ip, port):
		self.__set_esp_ip(ip)
		self.__set_esp_port(port)
		# TODO Dictionary must de completed.
		self.__text_to_orders = {
			"turn of the lights": "http://{0}:{1}/lightson".format(self.__esp_ip, self.__esp_port),
			"turn on the lights": "http://{0}:{1}/lightsoff".format(self.__esp_ip, self.__esp_port),
			"go to Canada": "http://{0}:{1}/gotocanada".format(self.__esp_ip, self.__esp_port)
		}
	def get_dictionary(self):
		return self.__text_to_orders

class Interpreter:
	"""
	Interpreter gives User interaction with Dictionary.
	TODO: In the future, interpreter will have to combine Comman execution and localization. Note that Interpreter will
	TODO: retrieve a functional url which will be called by Interpreter consumer.
	"""
	def __init__(self):
		self.__dict = Dictionary()

	def translate_command(self, text_order):
		"""
		Always set_located_esp32 before retrieving functional URL.
		:param text_order:
		:return: Desired URL pointing to right ESP32 and it's correct function.
		"""
		return self.__dict.get_dictionary()[text_order]

	def set_located_esp32(self, esp_ip, esp_port):
		"""
		Use location paradigm output to define which esp32 will receive the command.
		:param esp_ip: IP associated to decided ESP32.
		:param esp_port: PORT that will be open on ESP32 in order to recieve orders.
		:return: 200 if OK. TODO: treat errors!
		"""
		self.__dict.set_dictionary(esp_ip, esp_port)
		return 200


