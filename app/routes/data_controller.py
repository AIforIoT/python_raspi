#!/usr/bin/python3
from flask import Blueprint, request
import numpy as np
from app.models.data_request_object import FrameData
from app.processor.process_info import Info_processor
import xmlrpc.client
import json
#from gpiozero import LED

bp = Blueprint('data_controller', __name__)

info_processor = Info_processor()
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


@bp.route('/audio', methods=['POST'])
def get_audio():
    """
    ESP32 is sending us audio buffer!

    :return: 200 OK
    """
    global keyword_found

    print(request.data)

    rdata = json.loads(request.data.decode('utf-8'))
    ide = request.remote_addr
    data = rdata['data']
    eof = rdata['EOF']
    loca = rdata['location']

    if ide not in buffersDict:
        buffersDict[ide] = np.ndarray([BUFFER_MAX_SIZE])
        positionsDict[ide] = 0

    if not keyword_found:  # No keyword detected yet, fill up the buffer and send it to the keyword spotting module
        # data = request.data.split(b',')
        for d in data:
            byte = 0
            try:
                byte = int(d)
                buffersDict[ide][int(positionsDict[ide])] = byte
                positionsDict[ide] += 1
                if positionsDict[ide] >= BUFFER_MAX_SIZE:
                    # KeyWord Spotting
                    to_send = FrameData(np.array2string(buffersDict[ide]), ide, str(positionsDict[ide]))
                    client = xmlrpc.client.ServerProxy("http://localhost:8082/api")
                    response = client.send_data_request_object(to_send)

                    keyword_found = response.iouti
                    
                    if keyword_found:
                        #green.on()
                        pass
                    # Truncate
                    buffersDict[ide][0:int(BUFFER_MAX_SIZE / 2)] = buffersDict[ide][int(BUFFER_MAX_SIZE / 2):]
                    positionsDict[ide] = int(BUFFER_MAX_SIZE / 2)
            except:
                print("Error.... byte not int")
               
    else:
        if ide not in commandsBufferDict:
            commandsBufferDict[ide] = np.ndarray([BUFFER_CMD_MAX_SIZE])
            commandsPositionDict[ide] = 0

        # data = request.data.split(b',')
        for d in data:
            byte = 0
            try:
                byte = int(d)
            except ValueError:
                print("Error.... byte not int")
            
            commandsBufferDict[ide][int(commandsPositionDict[ide])] = byte
            commandsPositionDict[ide] += 1
            
            if commandsPositionDict[ide] == BUFFER_CMD_MAX_SIZE:  # The buffer can overflow here!!
                print("BUG! Buffer is full! Exiting 'for' statement to not crash")
                break

    if not eof and not commandsPositionDict[ide]:
        print("End sending cmd")

        to_send = FrameData(np.array2string(commandsBufferDict[ide]), ide, str(commandsPositionDict[ide]),'1')
        client = xmlrpc.client.ServerProxy("http://localhost:8082/api")
        response = client.send_data_request_object(to_send)
        info_processor.process_AI_data(response)
        
        keyword_found = False
        commandsPositionDict[ide] = 0
        positionsDict[ide] = 0

        #green.off()
        
    return "200", "OK"

"""
@bp.route('/audio/end', methods=['POST'])
def end_sending():

    global keyword_found, green

    rdata = json.loads(request.data)
    ide = rdata['ide']
    data = rdata['data']

    if ide not in commandsBufferDict:
        commandsBufferDict[ide] = np.ndarray([BUFFER_CMD_MAX_SIZE])
        commandsPositionDict[ide] = 0

    # data = request.data.split(b',')
    for d in data:
        byte = 0
        try:
            byte = int(d)
        except ValueError:
            print("Error.... byte not int")

        commandsBufferDict[ide][int(commandsPositionDict[ide])] = byte
        commandsPositionDict[ide] += 1

        if commandsPositionDict[ide] == BUFFER_CMD_MAX_SIZE:  # The buffer can overflow here!!
            print("BUG! Buffer is full! Exiting 'for' statement to not crash")
            break

    if commandsPositionDict[ide] is not 0:
        print("End sending cmd")

        to_send = FrameData(np.array2string(commandsBufferDict[ide]), ide, str(commandsPositionDict[ide]))
        client = xmlrpc.client.ServerProxy("http://localhost:8082/api")
        client.send_data_request_object(to_send)

    keyword_found = False
    commandsPositionDict[ide] = 0
    positionsDict[ide] = 0

    #green.off()
    return "200", "OK"
"""