from rpc_api import handler
from app.database.db_service import DBService
from app.models.data_request_object import ConfigParams, FrameData, DEFAULT_TYPES
from flask_xmlrpcre.xmlrepcre import Fault

import numpy as np
import json

'''
To make a method of the rpc_api server accessible from outside it is necessary to add the decorator '@handler.register'
to the function. 
'''

db_service = DBService()

@handler.register
def send_data_request_object(data_request_object):
    try:
        if type(data_request_object) != FrameData: return 400, 'data_request_object must be a FrameData type'

        #Deserialize data_request object
        config_params = data_request_object['_FrameData__config_params']

        numpy_data = data_request_object['_FrameData__numpy_data']
        r = numpy_data.replace("'",'')
        numpy_data = json.loads(r)
        numpy_data = np.array(numpy_data)

        print("TEST:")
        print(type(numpy_data) != 'numpy.ndarray')

        if type(numpy_data) == 'numpy.ndarray':
            db_service.save_FrameData(data_request_object)
        else:
            return 400, 'Numpy data type must be "numpy.ndarray" object'

        #TODO: save data_request_object in the db
            #Check the esp_id one of the registered esps contained in the 'esp_data' table.
            #IF there is already a data_request_object for esp_id, replace it with the new data
            #Else create new entry

    except Exception:
        return 400, 'Bad request'

    return 200, 'OK'

