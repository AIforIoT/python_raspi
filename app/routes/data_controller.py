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

BUFFER_MAX_SIZE = 16000  # Size of the buffer (To be changed)
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

    ide = request.remote_addr
    data = request.data

    # 20 bytes of data include 10 samples of audio (8 bit + 8 bit = 16 bit sample) - 15 bit are useful, 16 bit is 1 but never used. [1:16]
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

        # No keyword detected, fill the buffer and send it to the keyword spotting module
        if not keyword_found:

            # Feed the buffer with the byte
            feed_keyword_buffer(ide, byte)

            # If the buffer is full
            if positionsDict[ide] >= BUFFER_MAX_SIZE:
                try:
                    # Check if the buffer contains the keyword
                    response = send_to_ai(0, ide)
                    keyword_found = response.iouti

                except Exception as e:
                    print(e)

                # If the keyword is found
                if keyword_found:

                    # Create the command buffer if it does not exist for this ESP IDE
                    if ide not in commandsBufferDict:
                        commandsBufferDict[ide] = np.ndarray([BUFFER_CMD_MAX_SIZE])

                    # Once the keyword has been found, fill the commands buffer with the samples of the keyword buffer (do not miss anything)
                    #commandsBufferDict[ide][0:positionsDict[ide]] = np.copy(buffersDict[ide][0:positionsDict[ide]])
                    commandsPositionDict[ide] = positionsDict[ide]

                    # Clean keyword buffer
                    #buffersDict[ide][0:] = 0
                    #positionsDict[ide] = 0
					
                    #print("COMMAND POSITION: {}".format(commandsPositionDict[ide]))

        # If the keyword is found, feed the command buffer
        else:
            feed_command_buffer(ide, byte)

            # If the command buffer is full
            if commandsPositionDict[ide] >= BUFFER_CMD_MAX_SIZE:
                try:
                    # Check if the buffer contains any command
                    response = send_to_ai(1, ide)

                    # If the response has not been understood as a real command ('E')
                    action = response.__dict__['_outputMessage__status']
                    print("Action: " + str(action))

                    # An action has been understood by AI, stop processing the audio data and process the new info
                    if action == 'H' or action == 'L':
                        info_processor.process_AI_data(response)

                        # Clean command buffer
                        #commandsBufferDict[ide][0:] = 0
                        #commandsPositionDict[ide] = 0

                except Exception as e:
                    print(e)

    # If EOF and the keyword is found (command buffer not full)
    if eof is '1' and keyword_found:
        try:
            # Try to process LAST audio
            response = send_to_ai(keyword_found, ide)

            # If the response has no valuable data reset all buffers, counters and keyword_found values
            action = response.__dict__['_outputMessage__status']
            print("Action: "+str(action))

            if action == 'H' or action == 'L': #An action has been understood by AI, stop processing the audio data and process the new info
                info_processor.process_AI_data(response)

            else:
                #If it is the last frame and there has been no valid command found, start process again
                info_processor.request_volume()

        except Exception as e:
            print(e)

        # Clean command buffer and reset keyword_found
        #commandsBufferDict[ide][:] = 0
        #commandsPositionDict[ide] = 0
        keyword_found = 0


    elif eof is '1' and not keyword_found:

        #If it is the last frame and there has been no keyword found, start process again: request volume to all ESPs
        info_processor.request_volume()

        # Clean command buffer and reset keyword_found
        buffersDict[ide][:] = 0
        positionsDict[ide] = 0
        keyword_found = 0

        # Call keyword detector of the buffer if it has been said TODO 

    return "OK", 200


def feed_keyword_buffer(ide, data):
    if ide not in buffersDict:
        buffersDict[ide] = np.ndarray([BUFFER_MAX_SIZE])
        positionsDict[ide] = 0

    if positionsDict[ide] < BUFFER_MAX_SIZE:
        buffersDict[ide][int(positionsDict[ide])] = data
        positionsDict[ide] += 1


def feed_command_buffer(ide, data):
    if ide not in commandsBufferDict or ide not in commandsPositionDict:
        commandsBufferDict[ide] = np.ndarray([BUFFER_CMD_MAX_SIZE])
        commandsPositionDict[ide] = 0

    if commandsPositionDict[ide] < BUFFER_CMD_MAX_SIZE:
        commandsBufferDict[ide][int(commandsPositionDict[ide])] = data
        commandsPositionDict[ide] += 1


def send_to_ai(keyword, ide):
    printPurple("AI")

    if not keyword:
        c_buffer = np.copy(buffersDict[ide])
        c_offset = np.copy(positionsDict[ide])
        # Truncate
        #buffersDict[ide][0:int(BUFFER_MAX_SIZE / 2)] = buffersDict[ide][int(BUFFER_MAX_SIZE / 2):]
        #buffersDict[ide][int(BUFFER_MAX_SIZE / 2):] = 0
        #positionsDict[ide] = int(BUFFER_MAX_SIZE / 2)
        positionsDict[ide] = 0
        return send_data_request_object(c_buffer, ide, str(c_offset), keyword)

    else:
        c_buffer = np.copy(commandsBufferDict[ide])
        c_offset = np.copy(commandsPositionDict[ide])
        # It is not necessary to truncate as the response to the command buffer will be unique (Error or understood)
        #commandsBufferDict[ide][:] = 0
        commandsPositionDict[ide] = 0
        return send_data_request_object(c_buffer, ide, str(c_offset), keyword)
        #return send_data_request_object(commandsBufferDict[ide], ide, str(commandsPositionDict[ide]), keyword)

def printPurple(phrase):
    print('\033[95m'+phrase+'\033[0m')
