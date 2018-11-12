#!/usr/bin/python3
from flask import Blueprint, request
import numpy as np
from app.models.data_request_object import FrameData
import xmlrpc.client
import json
from gpiozero import LED

bp = Blueprint('data_controller', __name__)

BUFFER_MAX_SIZE = 16000  # Size of the buffer (To be changed)
BUFFER_CMD_MAX_SIZE = 64000  # Size of the buffer that will save the whole audio. (To be changed)

# Declare buffers
buffersDict = dict()
positionsDict = dict()
commandsBufferDict = dict()
commandsPositionDict = dict()

keyword_found = False
led = LED(4)


@bp.route('/audio', methods=['POST'])
def get_audio():
    """
    ESP32 is sending us audio buffer!

    :return: 200 OK
    """
    global keyword_found

    rdata = json.loads(request.data)
    ide = rdata['ide']
    data = rdata['data']

    if ide not in buffersDict:
        buffersDict[ide] = np.ndarray([BUFFER_MAX_SIZE])
        positionsDict[ide] = 0

    if not keyword_found:  # No keyword detected yet, fill up the buffer and send it to the keyword spotting module
        # data = request.data.split(b',')
        for d in data:
            byte = 0
            try:
                byte = int(d)
            except:
                print("Error.... byte not int")
            buffersDict[ide][int(positionsDict[ide])] = byte
            positionsDict[ide] += 1
            if positionsDict[ide] >= BUFFER_MAX_SIZE:
                # KeyWord Spotting
                to_send = FrameData(np.array2string(buffersDict[ide]), ide, str(positionsDict[ide]))
                client = xmlrpc.client.ServerProxy("http://localhost:8082/api")
                client.hello(to_send)

                # Truncate
                buffersDict[ide][0:int(BUFFER_MAX_SIZE / 2)] = buffersDict[ide][int(BUFFER_MAX_SIZE / 2):]
                positionsDict[ide] = int(BUFFER_MAX_SIZE / 2)

    else:
        # Speech to text? -> Other buffer
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

    print(positionsDict[ide])
    print(buffersDict[ide])
    return "200"


@bp.route('/audio/end', methods=['POST'])
def end_sending():
    """
    The tx was ended, its time to speech recognition!
    For esp32 speech buffer calculate the one with more power and send it to the speech recognition engine.

    :return: 200 OK ot 500 Error
    """
    global keyword_found, led

    rdata = json.loads(request.data)
    ide = rdata['ide']
    data = rdata['data']

    if commandsPositionDict[ide] is not 0:
        print("End sending cmd")

        to_send = FrameData(np.array2string(commandsBufferDict[ide]), ide, str(commandsPositionDict[ide]))
        client = xmlrpc.client.ServerProxy("http://localhost:8082/api")
        client.hello(to_send)

    keyword_found = False
    commandsPositionDict[ide] = 0
    positionsDict[ide] = 0

    led.off()
    return "200", "OK"


@bp.route('/keyword_detected', methods=['GET'])
def keyword_detector():
    global keyword_found, led

    led.on()
    keyword_found = True
    return "200"


