#!/usr/bin/python3
from flask import Blueprint, request
import numpy as np
from app.models.data_request_object import FrameData
from app.processor.process_info import Info_processor
import xmlrpc.client
import json
import os
from app.AI.AI_service import send_data_request_object

#from gpiozero import LED

bp = Blueprint('data_controller', __name__)

info_processor = Info_processor()
BUFFER_MAX_SIZE = 32000  # Size of the buffer (To be changed)
BUFFER_CMD_MAX_SIZE = 64000  # Size of the buffer that will save the whole audio. (To be changed)

# Declare buffers
buffersDict = dict()
positionsDict = dict()
commandsBufferDict = dict()
commandsPositionDict = dict()

keyword_found = False
#green = LED(4)
#red = LED(3)


@bp.route('/audio/<esp_id>/<eof>', methods=['POST'])
def get_binary_audio(esp_id, eof):
    # ESP32 is sending audio buffer!
    
    global keyword_found
    #global counter

    ide = request.remote_addr
    data = request.data
    
    #print("Dades rebudes: {}".format(str(data)))
    #myfile = open("/home/pi/Desktop/python_raspi/app/routes/audio_input"+str(counter)+".txt", "a")
    #myfile.write(str(data))  
            
    # 20 bytes of data include 10 samples of audio (8 bit + 8 bit = 16 bit sample) - 15 bit are useful, 16 bit is 1 but never used. [1:16]
    for i in range(int(len(data)/2)):
        try:

            # Join the two bytes received into a string and include the 0 necessary for 16 bit variable
            byte = ''.join([str(0)]*(8-len(bin(data[i*2])[2:]))) + bin(data[i*2])[2:] + ''.join([str(0)]*(8-len(bin(data[i*2+1])[2:]))) + bin(data[i*2+1])[2:]      
            
            # print binary value
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

            
            #myfile.write(str(byte))
            #myfile.write("\n")

        except Exception as e:
            print("Error Interpreting values!")
            print(e)
            byte=0

        if not keyword_found:  # No keyword detected yet, fill up the buffer and send it to the keyword spotting module
            feed_keyword_buffer(ide, byte)
            if positionsDict[ide] >= BUFFER_MAX_SIZE-1:
                # KeyWord Spotting
                try:
                    response = send_to_ai(0, ide)
                    keyword_found = response.iouti
                except Exception as e:
                    print(e)

                if keyword_found:
                    #Clean keyword buffer
                    buffersDict[ide][0:] = 0
                    positionsDict[ide] = 0
                    pass

                else:
                    #When trying to detect the keyword and not found, move the buffer data and start storing the next data from the middle to the end. (Resetting the values to be filled)
                    buffersDict[ide][0:int(BUFFER_MAX_SIZE/2-1)] = buffersDict[ide][int(BUFFER_MAX_SIZE/2):]
                    buffersDict[ide][int(BUFFER_MAX_SIZE/2):] = 0
                    positionsDict[ide] = int(BUFFER_MAX_SIZE/2)

                """ Aixo produeix error al agafar les requests de forma asincrona
                else:
                    # Truncate
                    buffersDict[ide][0:int(BUFFER_MAX_SIZE / 2)] = buffersDict[ide][int(BUFFER_MAX_SIZE / 2):]
                    positionsDict[ide] = int(BUFFER_MAX_SIZE / 2)
                """

        else:
            feed_command_buffer(ide, byte)
            if commandsPositionDict[ide] >= BUFFER_CMD_MAX_SIZE-1:
                #Buffer with command is empty
                try:
                    #Try to process audio
                    response = send_to_ai(keyword_found, ide)

                    #If the response has no valuable data, continue listening
                    action = response.__dict__['_outputMessage__status']

                    if not action == 'E': #An action understood by AI, stop processing the data and process the new info
                        info_processor.process_AI_data(response)
                        return

                    else:
                        #Continue trying to understand command
                        commandsBufferDict[ide][0:int(BUFFER_CMD_MAX_SIZE/2-1)] = commandsBufferDict[ide][int(BUFFER_CMD_MAX_SIZE/2):]
                        commandsBufferDict[ide][int(BUFFER_CMD_MAX_SIZE/2):] = 0
                        commandsPositionDict[ide] = int(BUFFER_CMD_MAX_SIZE/2)

                except Exception as e:
                    print(e)

    if eof is '1' and keyword_found:
        print("End sending cmd")
        try:
            #Try to process LAST audio
            response = send_to_ai(keyword_found, ide)

            #If the response has no valuable data reset all buffers, counters and keyword_found values
            action = response.__dict__['_outputMessage__status']
            if not action == 'E': #An action understood by AI, stop processing the data and process the new info
                info_processor.process_AI_data(response)

        except Exception as e:
            print(e)

        #If it is the last frame and there has been no valid command found, start process again
        info_processor.request_volume()

        keyword_found = 0
        commandsBufferDict[ide][0:] = 0
        positionsDict[ide] = 0

    elif eof is '1' and not keyword_found:
        '''
        print("End sending keyword")

        try:
            response = send_to_ai(keyword_found, ide)
            keyword_found = response.iouti
        except Exception as e:
            print(e)
        '''
        #If it is the last frame and there has been no keyword found, start process again
        info_processor.request_volume()

        #End of file and keyword has not been found - Reset keyword buffer and its position counter, and request volume to all ESPs
        buffersDict[ide][0:] = 0
        positionsDict[ide] = 0
        commandsPositionDict[ide] = 0
    
    return "OK", 200


def feed_keyword_buffer(ide, data):
    if ide not in buffersDict:
        buffersDict[ide] = np.ndarray([BUFFER_MAX_SIZE])
        positionsDict[ide] = 0
    if positionsDict[ide] < BUFFER_MAX_SIZE-1:
        buffersDict[ide][int(positionsDict[ide])] = data
        positionsDict[ide] += 1


def feed_command_buffer(ide, data):
    if ide not in commandsBufferDict:
        commandsBufferDict[ide] = np.ndarray([BUFFER_CMD_MAX_SIZE])
        commandsPositionDict[ide] = 0

    if commandsPositionDict[ide] < BUFFER_CMD_MAX_SIZE-1:
        commandsBufferDict[ide][int(commandsPositionDict[ide])] = data
        commandsPositionDict[ide] += 1

    '''    
    if commandsPositionDict[ide] >= BUFFER_CMD_MAX_SIZE-1:  # The buffer can overflow here!!
        printPurple("BUG! Buffer is full! Exiting 'for' statement to not crash")
        return
    '''


def send_to_ai(keyword, ide):
    printPurple("AI")

    if not keyword:
        # Adicio per possible solucio del problema
        c_buffer = buffersDict[ide]
        c_offset = positionsDict[ide]
        # Truncate
        #buffersDict[ide][0:int(BUFFER_MAX_SIZE / 2)] = buffersDict[ide][int(BUFFER_MAX_SIZE / 2):]
        #positionsDict[ide] = int(BUFFER_MAX_SIZE / 2)
        positionsDict[ide] = 0
        return send_data_request_object(c_buffer, ide, str(c_offset), keyword)
        # Fi 
        #return send_data_request_object(buffersDict[ide], ide, str(positionsDict[ide]), keyword)
    else:
        return send_data_request_object(commandsBufferDict[ide], ide, str(positionsDict[ide]), keyword)

def printPurple(phrase):
    print('\033[95m'+phrase+'\033[0m')


def reset_all_buffers_data():
    keyword_found = 0
    buffersDict = 0
    positionsDict = 0
    commandsBufferDict = 0
    commandsPositionDict = 0