from app.database.database import db_session
from app.database.models import SQLFrame, ESPdata, VOLUMEdata
from sqlalchemy import desc, asc, func, select
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

    #Update a registered ESP data by esp_id
    def update_registered_esp(self, esp_to_update):

        count = ESPdata.query.filter_by(esp_id=esp_to_update.esp_id).count()
        db_session.commit()

        if(count==0):
            return
        obj = ESPdata.query.filter_by(esp_id=esp_to_update.esp_id).one()

        if(obj is not None):
            print("tnt")
            db_session.delete(obj)
            db_session.commit()
        self.register_esp(esp_to_update)


    def is_esp_id_present(self, esp_id):
        esps = ESPdata.query.filter_by(esp_id=esp_id).all()
        db_session.commit()
        if(len(esps)==0):
            return False
        else:
            return True

    #Delete all ESPdata entities stored in the db #####
    def delete_all_ESPs(self):
        num_rows_deleted = db_session.query(ESPdata).delete()
        db_session.commit()
        return num_rows_deleted

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
    
    ### --- NEW --- ###
    def update_registered_esp_volume_data(self, volume_data):
        count =VOLUMEdata.query.filter_by(esp_id=volume_data.esp_id).count()
        db_session.commit()

        if(count==0):
            return
        obj = VOLUMEdata.query.filter_by(esp_id=volume_data.esp_id).one()

        if(obj is not None):
            print("tnt")
            db_session.delete(obj)
            db_session.commit()
        self.save_volume_data(volume_data)

    def is_esp_id_present_in_volume(self, esp_id):
        vols = VOLUMEdata.query.filter_by(esp_id=esp_id).all()
        db_session.commit()
        if(len(vols)==0):
            return False
        else:
            return True
    ##################


    
    #Delete all volume_data entities stored in the #####
    def delete_all_volumes(self):
        num_rows_deleted = db_session.query(VOLUMEdata).delete()
        db_session.commit()
        return num_rows_deleted


    #Return a list with all stored volumes #####
    def get_all_volumes(self):
        results = VOLUMEdata.query.all()
        volumes = []
        for result in results:
            esp = mapper.VOLUMEdata_to_volume_data(result)
            volumes.append(esp.__dict__)
        return volumes


    #Get in the 'frame_data' table the SQLFrame with 'esp_id' and return its 'delay' field #####
    def get_delay_by_esp_id(self, esp_id):
        results = VOLUMEdata.query.filter_by(esp_id=esp_id)
        if results is None:
            return None
        for result in results:
            esp = mapper.VOLUMEdata_to_volume_data(result)
            return esp.__dict__['_Volume_data__delay']


    #Return the volume_data object with 'timestamp' and volume property is the max. #####
    def get_volume_data_by_timestamp_and_volume_is_max(self, timestamp):
        VOLdata = VOLUMEdata.query.filter_by(timestamp=timestamp).order_by(desc(VOLUMEdata.volume)).first()
        if VOLdata is None:
            return None
        volume_data = mapper.VOLUMEdata_to_volume_data(VOLdata)
        return volume_data.__dict__

    def get_esp_id_volume_max(self, type):
        VOLdata = VOLUMEdata.query.order_by(desc(VOLUMEdata.volume)).first()
        if VOLdata is None:
            return None     
        else:
            volume_data = mapper.VOLUMEdata_to_volume_data(VOLdata)
            esp_id = volume_data.esp_id
            for esp in self.get_esp_by_type(type):
                if str(esp_id) == (esp['_ESP_data__esp_ip']):
                    return esp_id
            return None



    #Return the volume_data object with 'timestamp' #####
    def get_all_volumes_by_timestamp(self, timestamp):
        results = VOLUMEdata.query.filter_by(timestamp=timestamp)
        if results is None:
            return None
        vol_list = []
        for result in results:
            vol = mapper.VOLUMEdata_to_volume_data(result)
            vol_list.append(vol.__dict__)
        return vol_list

    #Return the value of the most recent timestamp for all stored volumes.
    def get_last_timestamp(self):
        result = VOLUMEdata.query.order_by(desc(VOLUMEdata.timestamp)).first()
        if result is None:
            return None
        volume_data = mapper.VOLUMEdata_to_volume_data(result)
        return volume_data.__dict__['_Volume_data__timestamp']


    def get_volume_data_by_timestamp_and_esp_id_is_different(self, timestamp, esp_id):
        results = VOLUMEdata.query.filter_by(timestamp=timestamp).filter(VOLUMEdata.esp_id!=esp_id)
        if results is None:
            return None
        vol_list = []
        for result in results:
            vol = mapper.VOLUMEdata_to_volume_data(result)
            vol_list.append(vol.__dict__)
        return vol_list