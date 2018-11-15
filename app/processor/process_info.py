from app.database.db_service import DBService
from app.http_client.http_client_service import Http_service

db_service = DBService()
http_service = Http_service()

class Info_processor:

    def process_AI_data(self, AI_data):

        #TODO:
            #AI_data object get type (ei: light, blind, other): esp_type
            #AI_data -> is location required?
                #Yes:
                    #GET ESP 'timestamp' from the AI_data object
                    #volumes = db_service.get_all_volumes_by_timestamp(timestamp)
                    #localization.get_closest_esp_id(timestamp) -> Preguntar Miquel com va el seu modul d localització

                #No:
                    #AI_data get action (ei: ON/OFF)
                    #esps_with_requested_type = db_service.get_esp_by_type(esp_type)
                        #http_service.send_http_action(esps_with_requested_type, action)

                    #esps_with_type_dif_from_requested = db_service.get_esp_with_type_different(esp_type)
                        #http_service.send_http_action(esps_with_type_dif_from_requested, action)

        pass