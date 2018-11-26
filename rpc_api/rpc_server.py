from rpc_api import handler
from app.database.db_service import DBService
from app.models.data_request_object import FrameData
from app.models.AI_outMessage import outputMessage
from flask_xmlrpcre.xmlrepcre import Fault

#Artificial Intelligence imports
from local_keyword_detection import detect_keyword as dk
from artificial_intelligence import detect_command as dc

from scipy.io.wavfile import write

import numpy as np
import json
import sys
import os
import glob

'''
To make a method of the rpc_api server accessible from outside it is necessary to add the decorator '@handler.register'
to the function.
'''

@handler.register
def send_data_request_object(data_request_object):

    #try:
        if (data_request_object['_FrameData__numpy_data'] == False):
            return 400, 'data_request_object must be a FrameData type'

        #if type(data_request_object) != FrameData: return 400, 'data_request_object must be a FrameData type'

        #Deserialize data_request object
        config_params = []
        config_params.append(data_request_object['_FrameData__esp_id'])
        config_params.append(data_request_object['_FrameData__offset'])
        config_params.append(data_request_object['_FrameData__iouti'])

        numpy_data = data_request_object['_FrameData__numpy_data']
        numpy_data = np.array(numpy_data)

        """

        folder_name = "audioRaspi"
        #Check if the folder where wavs are saved exists
        if((os.path.isdir('./'+folder_name)) == false):
            os.mkdir(folder_name)
        else:
            pass

        #Check if the folder is empty for selecting the correct index
        if not os.listdir('./audioRaspi'):
            index = 0
        else:
            list_files = glob.glob("/*.wav")
            latest_file = max(list_of_files, key=os.path.getctime)
            index = latest_file.split('_')[1]
            if(index == 5):
                index = 0
            else:
                index += 1

        #Generate the wav file with the appropiate index
        file_name = "audio_" + index + ".wav"
        rate = 16000
        write(file_name, rate, numpy_data)

        #Move wav file to folder where they are stored
        os.rename("./" + file_name, "./audioRaspi/" + file_name)

        """

        file_names_list = glob.glob(os.path.join("local_keyword_detection/audio", '*.wav'))

        #Calls to Artificial Intelligence block and create object to return
        if(config_params[2] == 1):
            iouti_boolean = dk.detect('biel_achant.wav')
            print(iouti_boolean)
            outputM = outputMessage(iouti_boolean,"","","")
            return outputM
        else:
            speech = dc.detect_cloud("light_switch_off.wav")
            outputM = outputMessage(speech[0],speech[1],speech[2],speech[3])
            return outputM

        #TODO: save data_request_object in the db
            #Check the esp_id one of the registered esps contained in the 'esp_data' table.
            #IF there is already a data_request_object for esp_id, replace it with the new data
            #Else create new entry

    #except Exception:
        #return 400, 'Bad request'

        return 200, 'OK'
