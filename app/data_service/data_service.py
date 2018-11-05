import json
from app.models.data_request_object import ConfigParams, FrameData, DEFAULT_TYPES
from app.models.data_request_object import ConfigParams, FrameData
from app.database.db_service import DBService
import numpy as np

db_service = DBService()

class Data_service:


    def process_impulse_data(self, impulse_data):

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


    def save_esp_setup_data(self, esp_data):

        jsonData = json.loads(esp_data)
        esp_id = jsonData['esp_id']
        esp_ip = jsonData['esp_ip']
        esp_type = jsonData['esp_type']
        esp_x_axis = jsonData['esp_x_axis']
        esp_y_axis = jsonData['esp_y_axis']
        esp_y_axis = jsonData['side']
        esp_y_axis = jsonData['location']

        #TODO: store data in a static db

