import json, time
from app.models.ESP_data import ESP_data
from app.database.db_service import DBService
import numpy as np
from threading import Timer

REQUEST_DATA_TIME=10.0
db_service = DBService()

class Data_service:

    #Parses the received 'impulse_data' into a FrameData object and send a db request to store it.
    def process_data(self, impulse_data):

        jsonData = json.loads(impulse_data)
        esp_id = jsonData['esp_id']
        timestamp = jsonData['timestamp']
        delay = jsonData['delay']
        power = jsonData['power']
        offset = jsonData['offset']
        data_type = 0

        #Dummy numpy object. TODO: Replace by real object with voice data
        numpy_data = np.empty([131295], dtype=int)
        numpy_data = np.array2string(numpy_data)

        data_frame = FrameData(numpy_data, data_type, esp_id, delay, power, offset, timestamp)

        #TEST DB:
        db_service.save_FrameData(data_frame)

        return data_frame


    def process_data_request(self, data):

        #TODO: data_type = 0:

        #TODO: data_type = 1:
        return None



    def save_esp_setup_data(self, esp_init_data):

        jsonData = json.loads(esp_init_data)
        esp_id = jsonData['esp_id']
        esp_ip = jsonData['esp_ip']
        esp_type = jsonData['esp_type']
        esp_x_axis = jsonData['esp_x_axis']
        esp_y_axis = jsonData['esp_y_axis']
        side = jsonData['side']
        location= jsonData['location']

        esp_to_register = ESP_data(esp_id, esp_ip, esp_x_axis, esp_y_axis, esp_type, side, location)

        db_service.register_esp(esp_to_register)

    def request_esp_data(self):
        print("TIME is: "+str(time.time()))


    def process_volume(self, data):

        jsonData = json.loads(data)
        esp_id = jsonData['esp_id']
        timestamp = jsonData['timestamp']
        delay = jsonData['delay']
        volume = jsonData['volume']


        db_service.save_volume_data(volume_data)

        #Timer executes func  after 30s
        t = Timer(REQUEST_DATA_TIME, self.request_esp_data)
        t.start()
        print("ESTOY HACIENDO OTRAS COSAS???")

        #TODO: check if there is the first timestamp for esp_id stored
            #If so:  wake up cron after 30ms

        #Store data in db


