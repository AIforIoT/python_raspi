import json, time
from app.models.ESP_data import ESP_data
from app.database.models import ESPdata
from app.models.volume_data import Volume_data


class Mapper:

    def ESPdata_to_ESP_data(self, ESPdata):
        return ESP_data(esp_id=ESPdata.esp_id, esp_ip=ESPdata.esp_ip, x=ESPdata.x, y=ESPdata.y, type=ESPdata.type, side=ESPdata.side, location=ESPdata.location)

    def VOLUMEdata_to_volume_data(self, VOLUMEdata):
        return Volume_data(esp_id=VOLUMEdata.esp_id, timestamp=VOLUMEdata.timestamp, delay=VOLUMEdata.delay, volume=VOLUMEdata.volume)