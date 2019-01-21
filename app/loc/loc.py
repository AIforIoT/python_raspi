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
        try:
            self.P.solve()
        except Exception as e:
            print("ERROR on solve!!!!!!!!!!!1111")
            print(e)
            return
        if self.target.loc.x is not None:
            x = self.target.loc.x
        else: 
            x = 0
        if self.target.loc.y is not None:
            y = self.target.loc.y
        else:
            y = 0          
        return x, y

    def get_x_y(self, type):
        anchors = []

        for esp in db.get_esp_by_type(type):
            anchors.append(esp["_ESP_data__esp_id"])

        self.add_anchors(anchors)
        self.add_measures(anchors)
        a,b = self.solve()
        return a,b

    def get_x_y_direct(self):
        try:
            print("Test oscarMiquel: :)")
            print(db.get_all_esps())
            for anchor in db.get_all_esps():
                x = float(anchor["_ESP_data__x"])
                y = float(anchor["_ESP_data__y"])
                self.P.add_anchor(anchor["_ESP_data__esp_id"], (x, y))
                measure = db.get_delay_by_esp_id(anchor["_ESP_data__esp_id"])
                if measure is not None:
                    measure = float(measure)/240000000
                    print("measure: "+str(measure))
                    self.target.add_measure(anchor["_ESP_data__esp_id"], measure)
                print("past get x_y direct. DONE")
            x, y = self.solve()
            print("loc.x = "+str(x)+". loc.y = "+str(y))
            return x, y
        except Exception as e:
            print(e)
            pass
    
