import json, time
from app.models.ESP_data import ESP_data
from app.models.volume_data import Volume_data
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


    def request_data_to_esp(self, timestamp):

        active_esp_with_max_volume = db_service.get_volume_data_by_timestamp_and_volume_is_max(timestamp)
        active_esps_volumes = db_service.get_all_volumes_by_timestamp(timestamp)


        for esp_volume in active_esps_volumes:
            if (esp_volume.get_volume == active_esp_with_max_volume.get_volume):
                #TODO: client: send http request to esp with info: I don't want your data
                None
            else:
                #TODO: client: send http request to esp with info: I DO want your data
                None

    def process_volume(self, data):

        jsonData = json.loads(data)
        esp_id = jsonData['esp_id']
        timestamp = jsonData['timestamp']
        delay = jsonData['delay']
        volume = jsonData['volume']

        #Save volume in db
        volume_data = Volume_data(esp_id, timestamp, delay, volume)
        db_service.save_volume_data(volume_data)

        #If it is the first volume received for 'timestamp', start timer
        if db_service.get_all_volumes_by_timestamp(timestamp) is None:
            #Delete previous db entries for past timestamps:
            db_service.delete_all_volumes()

            #Timer executes func  after 30ms
            t = Timer(REQUEST_DATA_TIME, self.request_data_to_esp, args=timestamp)
            t.start()
            print("vaig fent coses mentre m'espero a q salti el timer!")

        #TODO: check if there is the first timestamp for esp_id stored
            #If so:  wake up cron after 30ms

        #Store data in db


