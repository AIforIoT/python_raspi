import unittest
from mock import MagicMock
from app.processor.process_info import Info_processor
from app.database.db_service import DBService


info_processor = Info_processor()
db_service = DBService()

#Test the process_info.py class
class Test_info_process(unittest.TestCase):

    db_service.method = MagicMock(return_value=4)
    #test method process_AI_data
    def test_process_AI_data(self):


        self.assertEqual(fun(3), 4)