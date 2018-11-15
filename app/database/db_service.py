from app.database.database import db_session, engine
from app.database.models import SQLFrame, ESPdata
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

        #db object
        sqlframe = SQLFrame(numpy_data, esp_id, delay, power, offset, timestamp)

        #This code save the SQLFrame in the db with no checks.
        db_session.add(sqlframe)
        db_session.commit()

        #TODO refactor the data above to take into account the following info:
        #If there is already a SQLframe object with 'esp_id' registered in the database:
        #update field
        #ELSE save as new entry


    #This method is a test that gets all SQLFrame entities stored in the db and print its numpy_data object.
    def print_all_registered_SQLFrame(self):
        results = SQLFrame.query.all()
        for frame in results:
            frame = frame.__dict__
            numpy_data = frame['_FrameData__numpy_data']
            print(numpy_data)

    #Get in the 'esp_data' table the ESPdata object with 'esp_id', and return its coordenates (x, y)
    def get_coordenates_by_esp_id(self, esp_id):

        #TODO: check in 'esp_data' table if there is a ESPdata stored object with 'esp_id':
        #IF SO:
        #GET ESPdata object and return attributes x and y.
        #ELSE 'NOT FOUND' -> no dafa found for 'esp_id'

        x = 3
        y = 4
        return x, y


    #Get in the 'frame_data' table the SQLFrame with 'esp_id' and return its 'delay' field
    def get_delay_by_esp_id(self, esp_id):

        #TODO: check in 'frame_data' table if there is a SQLFrame stored object with 'esp_id':
        #If so:
        #get the ESPdata frame and return the field 'delay'
        #ELSE 'NOT FOUND' -> no dafa found for 'esp_id'

        delay = 3820
        return delay

    #Register a new esp into de esp_data db table.
    def register_esp(self, esp_to_register):

        #Map ESP_data object into ESPdata entity
        esp_id = esp_to_register['_ESP_data__esp_id']
        esp_ip = esp_to_register['_ESP_data__esp_ip']
        x = esp_to_register['_ESP_data__x']
        y = esp_to_register['_ESP_data__y']
        esp_type = esp_to_register['_ESP_data__type']
        side = esp_to_register['_ESP_data__side']
        location = esp_to_register['_ESP_data__location']

        #Create ESPdata db entity
        sqlESPdata = ESPdata(esp_id, esp_ip, x, y, esp_type, side, location)
        db_session.add(sqlESPdata)
        db_session.commit()

    #Print in terminal all registered esp_id's
    def print_all_registered_esp_id(self):
        results = ESPdata.query.all()
        for esp in results:
            esp = esp.__dict__
            print(esp['__ESP_data__esp_id'])


    def save_volume_data(self, volume_data):
        #todo: save volume_data
        return None

    def delete_all_volumes(self):
        #todo: delete all volume_data entities stored in the db
        return None

    def get_volume_data_by_timestamp_and_volume_is_max(self, timestamp):
        #todo: Return the volume_data object with 'timestamp' and volume property is the max.
        return None

    def get_all_volumes_by_timestamp(self, timestamp):
        #todo: Return the volume_data object with 'timestamp'
        return None