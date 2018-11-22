from app.database.database import db_session
from app.database.models import SQLFrame, ESPdata
from sqlalchemy import desc

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

    def get_all_esps(self):
        #TODO: MIREU QUE AIXO SIGUI CORRECTE I BORREU EL WARNING XD!!!!!!!!!!!!!!!!!
        return ESPdata.query.all()

    def save_volume_data(self, volume_data):
        #todo: save volume_data
        sqlVOLUMEdata = VOLUMEdata(volume_data.esp_id, volume_data.timestamp, volume_data.delay, volume_data.volume)
        db_session.add(sqlVOLUMEdata)
        db_session.commit()
        pass

    def delete_all_volumes(self):
        #todo: delete all volume_data entities stored in the db
        pass

    def get_volume_data_by_timestamp_and_volume_is_max(self, timestamp):
        #todo: Return the volume_data object with 'timestamp' and volume property is the max.
        volume_data = VOLUMEdata.query.filter_by(timestamp=timestamp).order_by(desc(volume)).first()
        return volume_data

    def get_all_volumes_by_timestamp(self, timestamp):
        #todo: Return the volume_data object with 'timestamp'
        volume_data = VOLUMPEdata.query.filter_by(timestamp=timestamp)
        return volume_data

    def get_esp_by_type(self, type):
        #todo: from the registered esps, return a list with the ones with 'type'
        esps = ESPdata.query.filter_by(type=type)
        return esps

    def get_esp_with_type_different(self, type):
        #todo: return a list of esps with type field different from 'type'
        esps = ESPdata.query.filter(timestamp != timestamp)
        return esps

    def get_esp_with_esp_id_different_from(self, esp_id):
        #todo: return a list with all esp registered that esp_id field is different from 'esp_id'
        return None