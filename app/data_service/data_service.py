import json

class Data_service:

    def process_impulse_data(self, impulse_data):

        jsonData = json.loads(impulse_data)
        esp_id = jsonData['esp_id']
        delay = jsonData['delay']
        power = jsonData['power']
        data = jsonData['data']

        print(', esp_id: '+str(esp_id)+', delay: '+str(delay)+'pow: '+str(power)+', data: '+str(data))

        #TODO: redirect to impulse functionality
