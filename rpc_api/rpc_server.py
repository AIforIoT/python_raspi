from flask_xmlrpcre.xmlrepcre import Fault
from rpc_api import handler
from ..artificial_intelligence import main.py
import numpy as np
import json
import wavio
import os
import glob

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
        rate = 16000
        bytes_per_sample = 1 #8 bits

        #Create the directory where the audio files are stored (max 5)
        dirName = 'audio_files'
        try:
            os.mkdir(dirName)
        except FileExistsError:
            pass

        list_of_files = glob.glob('/' + dirName + "/*')

        if not list_of_files:
            index = 0
        else:
            latest_file = max(list_of_files, key=os.path.getctime)
            index = latest_file.split('_')
            #Check if the index is 5 and overwrite
            if index == 5:
                index = 0
            else:
                index += 1

        #Create wav file, store in the directory and transcribe
        name = "audio_" + index + ".wav"
        wavio.write(name, numpy_data, rate, bytes_per_sample)

        #Transcribe
        if(config_params.){

        }

        else{

        }
        transcription = detection(name)

    except Exception:
        return 400, 'Unable to deserialize data_request_object'

    return transcription
