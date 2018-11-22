import unittest
import mock
from mock import MagicMock
from app.processor.process_info import Info_processor
from app.database.db_service import DBService
from app.models.AI_outMessage import outputMessage
from app.database.models import ESPdata


info_processor = Info_processor()
db_service = DBService()

#Test the process_info.py class
class Test_info_process(unittest.TestCase):

    leftover_esp_list = []
    esp_1 = ESPdata(esp_id="192.168.1.12", esp_ip="192.168.1.12", x=3, y=4, type='light', side=None, location=None, delay=0, timestamp=1987654321)
    esp_2 = ESPdata(esp_id="192.168.1.14", esp_ip="192.168.1.14", x=6, y=4, type='blind', side=None, location=None, delay=0, timestamp=1987654321)
    leftover_esp_list.append(esp_1)
    leftover_esp_list.append(esp_2)

    db_service.get_last_timestamp = MagicMock(return_value=1987654321)
    db_service.get_esp_with_esp_id_different_from = MagicMock(return_value=leftover_esp_list)

    #test method process_AI_data
    def test_process_AI_data(self):

        iouti = False
        status = 1
        location= True
        typeObj = 'light'
        AI_data = outputMessage(iouti,status,location,typeObj)

        info_processor.process_AI_data(AI_data)