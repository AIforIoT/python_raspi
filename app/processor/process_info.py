from app.database.db_service import DBService
from app.http_client.http_client_service import Http_service

db_service = DBService()
http_service = Http_service()

class Info_processor:

    # This method takes the decision of which esp/s have to perform an action, and uses the http_client_service to inform
    # which requests should be done. Once the action has been performed, this method is also in charge of reporting to all
    # the leftover esps registered that its states must change to 'send volume'.
    def process_AI_data(self, AI_data):

        #TODO:
            #AI_data object get type (ei: light, blind, other): esp_type
            #AI_data -> is location required?
            #AI_data -> get action: High or Low -> Ara està com High=1, Low=0, es pot canviar!
                #Yes:
                    #GET ESP 'timestamp' from the AI_data object
                    #GET ESP 'esp_type' from the AI_data object
                    #x, y = localization.metode_que_no_se_quin_es_hehe(timestamp) -> aixo torna les coordenades x,y de la persona q esta parlant todo: Canviar a metode real
                    #esp_id =self.get_closest_esp_by_type(x, y, esp_type)

                    #http_service.send_http_action_to_esp_id(esp_id, action)
                    #leftover_esp_list = db_service.get_esp_with_esp_id_different_from(esp_id)
                    #http_service.request_esp_volumes(leftover_esp_list)

                #No:
                    #AI_data get action (ei: ON/OFF)
                    #esps_with_requested_type = db_service.get_esp_by_type(esp_type)
                        #http_service.send_http_action(esps_with_requested_type, action)

                    #esps_with_type_dif_from_requested = db_service.get_esp_with_type_different(esp_type)
                        #http_service.request_esp_volumes(esps_with_type_dif_from_requested)

        #When a decision has been taken: delete all volume entries in the db.
        #db_service.delete_all_volumes()

        return 1

    #This method returns the esp_id of the closest esp to the position(x,y) that has 'type'
    def get_closest_esp_by_type(self, x, y, esp_type):
        #TODO
        #return esp_id_of_closest_esp_with_esp_type
        pass