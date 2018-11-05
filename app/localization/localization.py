import localization as lz
import sys
from app.database.db_service import DBService
db = DBService()

class Localization:
	# DEFINE CONSTANTS
	__SOUND_VEL=331 # TODO get this value from db or constants file
	__POSITION_TUPLE_DB="position_coord" # TODO this field must bet set accordingly to Database field titles
	__DELAY_DB="" # TODO this field must bet set accordingly to Database field titles
	# Testing: delays = [float(x) / __SOUND_VEL for x in sys.argv[1:]]
	P=None
	target=None
	label_target=None
	def __init__(self):
		"""
			Set mode for localization module.
		"""
		self.P=lz.Project(mode='2D',solver='LSE')
		self.target,self.label_target=P.add_target()

	def add_anchors(listAnchors):
		for anchor in listAnchors:
			self.P.add_anchor(anchor.str(), db.get_coordenates_by_esp_id(anchor.str()))

	
	def add_mesures():
		for anchor in listAnchors:
			self.P.add_measure(anchor.str(), db.get_delay_by_esp_id(anchor.str()))

	def solve():
		print(self.P.solve())
		return self.target.loc, self.label_target
