from rpc_api import handler
from app.database.db_service import DBService
from app.models.data_request_object import FrameData
from app.models.AI_outMessage import outputMessage
from flask_xmlrpcre.xmlrepcre import Fault

#Artificial Intelligence imports
from local_keyword_detection import detect_keyword as dk
from artificial_intelligence import detect_command as dc

#from scipy.io.wavfile import write
#from wavio import write
import wave

import numpy as np
import json
import sys
import os
import glob

'''
To make a method of the rpc_api server accessible from outside it is necessary to add the decorator '@handler.register'
to the function.
'''

def send_data_request_object(data, esp_id, offset, iouti):

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


        print(numpy_data)
        #Generate the wav file with the appropiate index
        #file_name = "audio_" + index + ".wav"
        rate = 16000
        #genFile(rate, 8, 1, numpy_data)
        wav = wave.open("audio5.wav", "wb")
        wav.writeframes(numpy_data)
        #write("audio4.wav",rate, numpy_data)
        wav.close()

        #Move wav file to folder where they are stored
        #os.rename("./" + file_name, "./audioRaspi/" + file_name)
        """
        

        #file_names_list = glob.glob(os.path.join("local_keyword_detection/audio", '*.wav'))
        
        #Calls to Artificial Intelligence block and create object to return
    if(iouti == 0):
        print("waiting iouti")
        iouti_boolean = dk.detect('biel_achant.wav')
        print(iouti_boolean)
        outputM = outputMessage(iouti_boolean,"","","")
        return outputM
    else:
        speech = dc.detect_cloud("light_switch_off.wav")
        outputM = outputMessage(False,str(speech[0]),str(speech[1]),str(speech[2]))
        return outputM
