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
        self.target,self.label_target=self.P.add_target()

    def add_anchors(self,listAnchors):
        for anchor in listAnchors:
            x,y = db.get_coordenates_by_esp_id(anchor)
            self.P.add_anchor(anchor, (float(x), float(y)))

    def add_measures(self,listAnchors):
        for anchor in listAnchors:
            self.target.add_measure(anchor, float(db.get_delay_by_esp_id(anchor)))

    def solve(self):
        self.P.solve()
        return self.target.loc, self.label_target

    def get_x_y(self, type):
        anchors = []

        for esp in db.get_esp_by_type(type):
            anchors.append(esp["_ESP_data__esp_id"])

        self.add_anchors(anchors)
        self.add_measures(anchors)
        a,b = self.solve()
        return a,b

    def get_x_y_direct(self,type):
        for anchor in db.get_esp_by_type(type):
            self.P.add_anchor(anchor["_ESP_data__esp_id"], (float(anchor["_ESP_data__x"]), float(anchor["_ESP_data__y"])))
            self.target.add_measure(anchor["_ESP_data__esp_id"], float(db.get_delay_by_esp_id(anchor["_ESP_data__esp_id"])))
        return self.solve()