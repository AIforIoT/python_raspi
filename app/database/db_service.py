from app.database.database import db_session, engine
from app.database.models import SQLFrame, ESPdata
from sqlalchemy import inspect
from sqlalchemy import MetaData

class DBService:


    #This method is a test that gets all SQLFrame entities stored in the db and print its numpy_data object.
    def print_all_registered_SQLFrame(self):
        results = SQLFrame.query.all()
        for frame in results:
            frame = frame.__dict__
            numpy_data = frame['_FrameData__numpy_data']
            print(numpy_data)

    #Get in the 'esp_data' table the ESPdata object with 'esp_id', and return its coordenates (x, y)
    def get_coordenates_by_esp_id(self, esp_id):

        esp_data = ESPdata.query.filter_by(esp_id=esp_id).first()
        if esp_data is None:
            return None
        x = esp_data.x
        y = esp_data.y
        return x, y


    #Get in the 'frame_data' table the SQLFrame with 'esp_id' and return its 'delay' field
    def get_delay_by_esp_id(self, esp_id):

        esp_data = ESPdata.query.filter_by(esp_id=esp_id).first()
        if esp_data is None:
            return None
        delay = esp_data.delay
        return delay

    #Register a new esp into de esp_data db table.
    def register_esp(self, esp_to_register):

        #Map ESP_data object into ESPdata entity
        esp_id = esp_to_register.esp_id
        esp_ip = esp_to_register.esp_ip
        x = esp_to_register.x
        y = esp_to_register.y
        esp_type = esp_to_register.type
        side = esp_to_register.side
        location = esp_to_register.location

        #Create ESPdata db entity
        sqlESPdata = ESPdata(esp_id, esp_ip, x, y, esp_type, side, location)
        db_session.add(sqlESPdata)
        db_session.commit()

    #Print in terminal all registered esp_id's
    def print_all_registered_esp_id(self):
        results = ESPdata.query.all()
        return results
        #for esp in results:
            #esp = esp.__dict__
            #print(esp['__ESP_data__esp_id'])


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