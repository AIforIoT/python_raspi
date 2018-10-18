import json
from app.models.data_request_object import ConfigParams, FrameData
import numpy as np

class Data_service:

    def process_impulse_data(self, impulse_data):

        jsonData = json.loads(impulse_data)
        esp_id = jsonData['esp_id']
        delay = jsonData['delay']
        power = jsonData['power']
        frame_id = jsonData['frame_id']
        offset = jsonData['offset']

        #Dummy numpy object. TODO: Replace by real object with voice data
        numpy_data = np.empty([2, 2], dtype=int).tostring()

        data_frame = FrameData(numpy_data, esp_id, frame_id, delay, power, offset)
        return data_frame
