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

        #TODO: Store the received data in the SQLAlchemy DB


    except Exception:
        return 'Unable to deserialize data_request_object', 400

    return 'OK', 200
