from app.database.db_service import DBService
from app.http_client.http_client_service import Http_service
from app.loc.loc import Localization
import logging, math

db_service = DBService()
localization = Localization()
http_service = Http_service()


class Info_processor:

    # This method takes the decision of which esp/s have to perform an action, and uses the http_client_service to inform
    # which requests should be done. Once the action has been performed, this method is also in charge of reporting to all
    # the leftover esps registered that its states must change to 'send volume'.
    def process_AI_data(self, AI_data):
        AI_data = AI_data.__dict__

        #AI_data object get type (ei: light, blind, other): esp_type
        typeObj = AI_data['_outputMessage__typeObj'].lower()
		
        #AI_data -> get action: High or Low -> High=1, Low=0
        action = AI_data['_outputMessage__status']
		
        #AI_data -> is location required?
        location_required = AI_data['_outputMessage__location']

        print("ACTION: " + str(action))
        print("LOCATION: " + str(location_required))
        print("TYPE: " + typeObj)

        if location_required == 'H':
            # GET ESP the most recent 'timestamp' from volumes
            timestamp = db_service.get_last_timestamp()

            # Get x,y coordenates from speaker
            try:
                x,y = localization.get_x_y_direct() #TODO: GET PARAMS!!!
                print(x)
                print(y)
                print(type(x))
                esp_id = self.get_closest_esp_by_type(x, y, typeObj)
                print(esp_id)
            except Exception as e:
                print("Can't locate the position")
                x, y = 1, 2
                esp_id = db_service.get_esp_id_volume_max(typeObj)

            print(esp_id)
            
			if esp_id is not None:
                http_service.send_http_action_to_esp_id(esp_id, action)

            self.request_volume()

        else: #location_required == 'L'
            
            esps_with_requested_type = db_service.get_esp_by_type(typeObj)
            http_service.send_http_action(esps_with_requested_type, action)
            self.request_volume()

        # When a decision has been taken: delete all volume entries in the db.
        num_rows_deleted = db_service.delete_all_volumes()


    def request_volume(self):
        http_service.request_esp_volumes(db_service.get_all_esps())
		
        # Delete all old volume entries in the db.
        num_rows_deleted = db_service.delete_all_volumes()

    # This method returns the esp_id of the closest esp to the position(x,y) that has 'type'
    def get_closest_esp_by_type(self, x, y, esp_type):
        dists_dict = {}
        for esp in db_service.get_esp_by_type(esp_type):
            dists_dict[esp["_ESP_data__esp_id"]] = math.sqrt((float(x) - float(esp["_ESP_data__x"]))**2 + (float(y) -     float(esp["_ESP_data__y"]))**2)

        ids=list(dists_dict.keys())
        distances=list(dists_dict.values())

        return ids[ distances.index(min(distances)) ]

