from app.http_client.client import HTTP_CLIENT

def enum(**enums):
    return type('Enum', (), enums)

DEFAULT_ACTIONS = enum(
    ON=1,
    OFF=0
)

REQUEST_PATH= enum(
    TURN_ON="/H",
    TURN_OFF="/L",
    DATA_ON="/data/on",
    DATA_OFF="/data/off",
    VOLUME="/volume"
)

http_client = HTTP_CLIENT()

class Http_service:

    #This method performs an http request to every esp contained in the 'list_esps' with and an action (ON/OFF)
    def send_http_action(self, list_esps, action):
        #todo: change esp.get_esp_id() for real method
        if action is DEFAULT_ACTIONS.ON:
            for esp in list_esps:
                http_client.send_GET_request(esp.get_esp_ip(), REQUEST_PATH.TURN_ON)

        elif action is DEFAULT_ACTIONS.OFF:
            for esp in list_esps:
                http_client.send_GET_request(esp.get_esp_ip(), REQUEST_PATH.TURN_OFF)


    #This method sends an http request to all esps in the 'list_esps' informing the status has to change to 'volume'.
    def request_esp_volumes(self, list_esps):
        for esp in list_esps:
            http_client.send_GET_request(esp.get_esp_ip(), REQUEST_PATH.VOLUME)


    #This method sends an http request to the esp with 'esp_ip' requesting for voice data
    def request_esp_data(self, esp_ip):
        http_client.send_GET_request(esp_ip, REQUEST_PATH.DATA_ON)


    #This method inform all esps in the 'list_esp' no data is requested
    def reject_esp_data(self, list_esps):
        for esp in list_esps:
            http_client.send_GET_request(esp.get_esp_ip(), REQUEST_PATH.DATA_OFF)
