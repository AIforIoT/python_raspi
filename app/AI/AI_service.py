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
    #Check if the folder where wavs are saved exists
    if((path.isdir(folder_name)) == false):
      os.mkdir(folder_name)
    else:
      pass

    #Check if the folder is empty for selecting the correct index
    if not os.listdir(folder_name):
      index = 0
    else:
      list_files = glob.glob(folder_name+"/*.wav")
      latest_file = max(list_of_files, key=os.path.getctime)
      index = latest_file.split('_')[1]
      if(index == 5):
        index = 0
      else:
        index += 1

    print(data)

    plt.plot(data)
    plt.show()

    array = list(map(int, data))

    # Values from 0,4096 to -1,1
    #scaled = translate(array, -np.max(np.abs(array)), np.max(np.abs(array)), -32767, 32767)

    print(array)

    # Scale those values to -32767 to 32767 (wav format)
    scaled = np.int16(array/np.max(np.abs(array)) * 32767)

    #write('test2.wav', 16000, scaled)
   


   #Move wav file to folder where they are stored
   #os.rename("./" + file_name, "./audioRaspi/" + file_name)


    #file_names_list = glob.glob(os.path.join("local_keyword_detection/audio", '*.wav'))
    #Calls to Artificial Intelligence block and create object to return
    if (iouti == 0):
        print("waiting iouti")
        iouti_boolean = dk.detect('biel_achant.wav')
        print(iouti_boolean)
        outputM = outputMessage(iouti_boolean,"","","")
        return outputM
    else:
        speech = dc.detect_cloud("light_switch_off.wav")
        outputM = outputMessage(False,str(speech[0]),str(speech[1]),str(speech[2]))
        return outputM
