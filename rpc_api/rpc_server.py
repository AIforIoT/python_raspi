from flask_xmlrpcre.xmlrepcre import Fault
from rpc_api import handler
import numpy as np
import json
'''
To make a method of the rpc_api server accessible from outside it is necessary to add the decorator '@handler.register'
to the function. 
'''

@handler.register
def send_data_request_object(data_request_object):
    try:
        #Deserialize data_request object
        config_params = data_request_object['_FrameData__config_params']
        numpy_data = data_request_object['_FrameData__numpy_data']
        numpy_data = np.array(numpy_data)
        data_type = data_request_object['_FrameData__data_type']


        print(data_type)
        print("data type: "+str(data_type))
        #TODO: do something with data_request_object

    except Exception:
        return 400, 'Unable to deserialize data_request_object'

    return 200, 'OK'

