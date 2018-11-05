from app.database.database import db_session, engine
from app.database.models import SQLFrame
from sqlalchemy import inspect
from sqlalchemy import MetaData
from app.models.data_request_object import FrameData, ConfigParams

class DBService:

    #TEST: This method save the frame_data in the sqlalchemy db and then, gets all the data stored in the db
    def save_FrameData(self, frame_data):

        frame_data = frame_data.__dict__

        #Deserialize data_request object
        numpy_data = frame_data['_FrameData__numpy_data']
        config_params = frame_data['_FrameData__config_params'].__dict__
        esp_id = config_params['_ConfigParams__esp_id']
        delay = config_params['_ConfigParams__delay']
        power = config_params['_ConfigParams__power']
        offset = config_params['_ConfigParams__offset']
        timestamp = config_params['_ConfigParams__timestamp']

        sqlframe = SQLFrame(numpy_data, esp_id, delay, power, offset, timestamp)
        db_session.add(sqlframe)
        db_session.commit()

        results = SQLFrame.query.all()
        for frame in results:
            frame = frame.__dict__
            numpy_data = frame['_FrameData__numpy_data']
            print(numpy_data)


    def get_coordenates_by_esp_id(self, esp_id):

        #TODO
        x = 3
        y = 4
        return x, y


    def get_delay_by_esp_id(self, esp_id):

        delay = 3820
        return delay