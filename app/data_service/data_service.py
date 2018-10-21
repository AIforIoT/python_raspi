import json
from app.models.data_request_object import ConfigParams, FrameData
import numpy as np

class Data_service:

    def process_impulse_data(self, impulse_data):

        jsonData = json.loads(impulse_data)
        esp_id = jsonData['esp_id']
        timestamp = jsonData['timestamp']
        delay = jsonData['delay']
        power = jsonData['power']
        offset = jsonData['offset']

        #Dummy numpy object. TODO: Replace by real object with voice data
        numpy_data = np.empty([131295], dtype=int).tolist()

        data_frame = FrameData(str(numpy_data), esp_id, delay, power, offset, timestamp)
        return data_frame
