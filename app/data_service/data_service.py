import json
from app.models.data_request_object import ConfigParams, FrameData
import numpy as np
from app.database.database import db_session
from app.database.models import User


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

        #DATABASE TEST:
        u = User('fuckumadafaka', 'admin@xaaaaaaaaaaaaat.zas')
        db_session.add(u)
        db_session.commit()

        print(User.query.all())

        data_frame = FrameData(str(numpy_data), esp_id, delay, power, offset, timestamp)
        return data_frame
