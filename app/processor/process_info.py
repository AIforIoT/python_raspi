from app.database.db_service import DBService
from app.http_client.http_client_service import Http_service
#from app.localization.localization import Localization
import logging, math
#from app.localization.localization import Localization
import logging
import math

db_service = DBService()
#localization = Localization()
http_service = Http_service()


class Info_processor:

    # This method takes the decision of which esp/s have to perform an action, and uses the http_client_service to inform
    # which requests should be done. Once the action has been performed, this method is also in charge of reporting to all
    # the leftover esps registered that its states must change to 'send volume'.
    def process_AI_data(self, AI_data):
        AI_data = AI_data.__dict__

        #AI_data object get type (ei: light, blind, other): esp_type
        typeObj = AI_data['device']
        #AI_data -> get action: High or Low -> High=1, Low=0
        action = AI_data['_outputMessage__status']
        #AI_data -> is location required?
        location_required = AI_data['_outputMessage__location']

        print("ACTION: " + str(action))
        print("LOCATION: " + str(location_required))

        if action == 'E':
            print("VOLUME REQUESTED BECAUSE OF ERROR")
            http_service.request_esp_volumes(db_service.get_all_esps())
            num_rows_deleted = db_service.delete_all_volumes()
            return

        if location_required == 'H' or location_required == 'L':
            #GET ESP the most recent 'timestamp' from volumes
            timestamp = db_service.get_last_timestamp()

            # Get x,y coordenates from speaker
            #x, y = localization.get_x_y() #TODO: GET PARAMS!!!
            x, y = 1, 2
            esp_id = self.get_closest_esp_by_type(x, y, typeObj)

            http_service.send_http_action_to_esp_id(esp_id, action)
            leftover_esp_list = db_service.get_esp_with_esp_id_different_from(esp_id)
            http_service.request_esp_volumes(leftover_esp_list)

        else: #location_required == False

            esps_with_requested_type = db_service.get_esp_by_type(typeObj)
            http_service.send_http_action(esps_with_requested_type, action)

            esps_with_type_dif_from_requested = db_service.get_esp_with_type_different(typeObj)
            http_service.request_esp_volumes(esps_with_type_dif_from_requested)

        #When a decision has been taken: delete all volume entries in the db.
        num_rows_deleted = db_service.delete_all_volumes()


    def request_volume(self):
        http_service.request_esp_volumes(db_service.get_all_esps())
        #Delete all old volume entries in the db.
        num_rows_deleted = db_service.delete_all_volumes()

    #This method returns the esp_id of the closest esp to the position(x,y) that has 'type'
    def get_closest_esp_by_type(self, x, y, esp_type):
        #return esp_id_of_closest_esp_with_esp_type
        dists_dict = {}
        for esp in db_service.get_esp_by_type(esp_type):
            dists_dict[esp["_ESP_data__esp_id"]] = math.sqrt((float(x) - float(esp["_ESP_data__x"]))**2 + (float(y) -     float(esp["_ESP_data__y"]))**2)

        print(dists_dict)
        ids=list(dists_dict.keys())
        distances=list(dists_dict.values())

        return ids[ distances.index(min(distances)) ]

