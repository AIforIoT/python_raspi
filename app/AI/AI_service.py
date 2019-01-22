from app.database.db_service import DBService
from app.models.data_request_object import FrameData
from app.models.AI_outMessage import outputMessage

#Artificial Intelligence imports
from local_keyword_detection import detect_keyword as dk
from artificial_intelligence import detect_command as dc

from scipy.io.wavfile import write

import numpy as np
import json
import sys
import os
from os import path
import glob


import matplotlib.pyplot as plt
'''
To make a method of the rpc_api server accessible from outside it is necessary to add the decorator '@handler.register'
to the function.
'''

PATH = path.dirname(path.realpath(__file__))

def send_data_request_object(data, esp_id, offset, iouti):

    folder_name = PATH+'/audio'
    
    # Check if the folder where wavs are saved exists
    if path.isdir(folder_name) == False:
        os.mkdir(folder_name)
    else:
        pass
    
    index = 0
    
    # Check if the folder is empty for selecting the correct index
    if not os.listdir(folder_name):
        index = 0
    else:
        # List the wav files in the audio folder
        list_files = glob.glob(folder_name+"/*.wav")

        # Get the last audio file created
        latest_file = max(list_files, key=os.path.getctime)

        # Get the index of this audio file
        index = int(latest_file.split('_')[2].replace(".wav",""))
        
        if index is 200:
            index = 0
        else:
            index += 1

    try:
        array = list(map(int, data))

        # Scale those values to -32767 to 32767 (wav format)
        scaled = np.int16([i * 2 for i in array])

        # Write the wav file
        wav_name = folder_name+'/audio_'+str(index)+'.wav'
        write(wav_name, 16000, scaled)

        print("WAV " + str(index) + " created")

    except:
        print("WAV can't be created, too few samples")

        # Redirect to the last file created
        wav_name = folder_name+'/audio_'+str(index-1)+'.wav'

   
    # Calls to Artificial Intelligence block and create object to return
    if iouti is 0:
        print("Calling local Keyword detector ...")
        iouti_boolean = dk.detect(wav_name)
		
        print("Keyword detected: " + str(iouti_boolean))
		
        outputM = outputMessage(iouti_boolean,"","","")
        return outputM
    else:
        print("Calling speech detector ...")
        speech = dc.detect_cloud(wav_name)
		
        outputM = outputMessage(False,str(speech[0]),str(speech[1]),str(speech[2]))
        return outputM