#!/usr/bin/python3
from flask import Blueprint, request
import numpy as np
from app.models.data_request_object import FrameData
from app.processor.process_info import Info_processor
from app.AI.AI_service import send_data_request_object

#from gpiozero import LED

bp = Blueprint('data_controller', __name__)

info_processor = Info_processor()
#info_processor.request_volume()

BUFFER_MAX_SIZE = 128000  # Size of the buffer (To be changed)

# Declare buffers
buffersDict = dict()
positionsDict = dict()

counter = 0

@bp.route('/audio/<esp_id>/<eof>', methods=['POST'])
def get_binary_audio(esp_id, eof):
#    global counter
#    print(counter)
#    counter += 1
#    return "OK", 200


#def nothing(self):
    # ESP32 is sending audio buffer!
    ide = request.remote_addr
    data = request.data
    for i in range(int(len(data)/2)):
        try:

            # Join the two bytes received into a string and include the 0 necessary for 16 bit variable
            byte = ''.join([str(0)]*(8-len(bin(data[i*2])[2:]))) + bin(data[i*2])[2:] + ''.join([str(0)]*(8-len(bin(data[i*2+1])[2:]))) + bin(data[i*2+1])[2:]

            # Print binary value
            #print(byte)

            # bit 15 has the sign
            sign = byte[1]

            # if the sign is 0, positive - map value to int with base 2
            if sign is '0':
                byte = int(byte[2:16], 2)

            # if the sign is 1, negative - ca2 (change 0 to 1 and add 1)
            else:
                byte = byte[2:16].replace('1','2').replace('0','1').replace('2','0')
                byte = -(int(byte[2:16], 2) + 1)

        except Exception as e:
            print("Error Interpreting values!")
            print(e)
            byte = 0

        feed_buffer(ide,byte)

    if eof=="1" or positionsDict[ide] >= BUFFER_MAX_SIZE:
        response = send_to_ai(1, ide)
        action = response.__dict__['_outputMessage__status']
        print("Action: " + str(action))

    return "OK", 200



def feed_buffer(ide, data):
    if ide not in buffersDict:
        buffersDict[ide] = np.ndarray([BUFFER_MAX_SIZE])
        positionsDict[ide] = 0

    if positionsDict[ide] < BUFFER_MAX_SIZE:
        buffersDict[ide][int(positionsDict[ide])] = data
        positionsDict[ide] += 1

def send_to_ai(keyword, ide):

    if keyword:
        c_buffer = np.copy(buffersDict[ide])
        c_offset = np.copy(positionsDict[ide])
        #buffersDict[ide][0:int(BUFFER_MAX_SIZE / 2)] = buffersDict[ide][int(BUFFER_MAX_SIZE / 2):]
        #buffersDict[ide][int(BUFFER_MAX_SIZE / 2):] = 0
        #positionsDict[ide] = int(BUFFER_MAX_SIZE / 2)
        positionsDict[ide] = 0
        return send_data_request_object(c_buffer, ide, str(c_offset), keyword)

 