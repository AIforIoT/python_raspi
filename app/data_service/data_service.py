import json, time
from app.models.ESP_data import ESP_data
from app.models.volume_data import Volume_data
from app.database.db_service import DBService
from app.http_client.http_client_service import Http_service
import numpy as np
from threading import Timer

REQUEST_DATA_TIME=10.0
db_service = DBService()
http_client = Http_service()

class Data_service:


    def save_esp_setup_data(self, esp_init_data):
     
        jsonData = json.loads(esp_init_data.decode("utf-8"))
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

        #TODO: change: active_esp_with_max_volume.get_volume and active_esp_with_max_volume.get_esp_id by real get methods

        active_esp_with_max_volume = db_service.get_volume_data_by_timestamp_and_volume_is_max(timestamp)
        active_esp_volumes_low_pw = db_service.get_volume_data_by_timestamp_and_volume_is_different(timestamp, active_esp_with_max_volume.get_volume)

        http_client.reject_esp_data(active_esp_volumes_low_pw)
        http_client.request_esp_data(active_esp_with_max_volume.get_esp_id)


    def process_volume(self, data):

        jsonData = json.loads(data)
        esp_id = jsonData['esp_id']
        timestamp = jsonData['timestamp']
        delay = jsonData['delay']
        volume = jsonData['volume']

        #If it is the first volume received for 'timestamp', start timer
        if db_service.get_all_volumes_by_timestamp(timestamp) is None:
            #Delete previous db entries for past timestamps:
            db_service.delete_all_volumes()

            #Timer executes func  after 30ms
            t = Timer(REQUEST_DATA_TIME, self.request_data_to_esp, args=timestamp)
            t.start()

        #Save volume in db
        volume_data = Volume_data(esp_id, timestamp, delay, volume)
        db_service.save_volume_data(volume_data)

