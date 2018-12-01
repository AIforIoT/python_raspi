from app.database.database import db_session
from app.database.models import SQLFrame, ESPdata, VOLUMEdata
from sqlalchemy import desc, asc
from app.data_service.mapper import Mapper

mapper = Mapper()

class DBService:

    #Register a new esp into de esp_data db table. #####
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

    #Return a list with all registered ESPs #####
    def get_all_esps(self):
        results = ESPdata.query.all()
        esp_list = []
        for result in results:
            esp = mapper.ESPdata_to_ESP_data(result)
            esp_list.append(esp.__dict__)
        return esp_list

    # return a list with all esp registered that esp_id field is different from 'esp_id' #####
    def get_esp_with_esp_id_different_from(self, esp_id):
        results = ESPdata.query.filter(ESPdata.esp_id!=esp_id).all()
        esp_list = []
        for result in results:
            esp = mapper.ESPdata_to_ESP_data(result)
            esp_list.append(esp.__dict__)
        return esp_list

    #from the registered esps, return a list with the ones with 'type' #####
    def get_esp_by_type(self, type):
        results = ESPdata.query.filter_by(type=type)
        esp_list = []
        for result in results:
            esp = mapper.ESPdata_to_ESP_data(result)
            esp_list.append(esp.__dict__)
        return esp_list

    #return a list of esps with type field different from 'type' #####
    def get_esp_with_type_different(self, type):
        results = ESPdata.query.filter(ESPdata.type != type)
        esp_list = []
        for result in results:
            esp = mapper.ESPdata_to_ESP_data(result)
            esp_list.append(esp.__dict__)
        return esp_list


    #Get in the 'esp_data' table the ESPdata object with 'esp_id', and return its coordenates (x, y) #####
    def get_coordenates_by_esp_id(self, esp_id):

        esp_data = ESPdata.query.filter_by(esp_id=esp_id).first()
        if esp_data is None:
            return None
        x = esp_data.x
        y = esp_data.y
        return x, y


    #save volume_data #####
    def save_volume_data(self, volume_data):
        sqlVOLUMEdata = VOLUMEdata(volume_data.esp_id, volume_data.timestamp, volume_data.delay, volume_data.volume)
        db_session.add(sqlVOLUMEdata)
        db_session.commit()


    #Delete all volume_data entities stored in the #todo
    def delete_all_volumes(self):
        VOLUMEdata.query.all().delete()


    #Get in the 'frame_data' table the SQLFrame with 'esp_id' and return its 'delay' field
    def get_delay_by_esp_id(self, esp_id):
        VOLdata = VOLUMEdata.query.filter_by(esp_id=esp_id)
        if VOLdata is None:
            return None
        volume_data = mapper.VOLUMEdata_to_volume_data(VOLdata)
        delay = volume_data.delay
        return delay




    def get_volume_data_by_timestamp_and_volume_is_max(self, timestamp):
        #todo: Return the volume_data object with 'timestamp' and volume property is the max.
        volume_data = VOLUMEdata.query.filter_by(timestamp=timestamp).order_by(desc(volume)).first()
        return volume_data

    def get_all_volumes_by_timestamp(self, timestamp):
        #todo: Return the volume_data object with 'timestamp'
        volume_data = VOLUMEdata.query.filter_by(timestamp=timestamp)
        return volume_data

    def get_last_timestamp(self):
        volume_data = VOLUMEdata.query.order_by(asc(timestamp)).first()
        return volume_data.timestamp




