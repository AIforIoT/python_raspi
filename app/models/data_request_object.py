import os

DEFAULT_TYPES = {
    "IOUTI": 0,
    "VOICE_DATA": 1
}

'''
The object FrameData must contain all the information about a frame. 
The ConfigParams object must contain the following information: esp_id, delay, power and offset. All this 
values must be stored as string.
The numpy_data object must be a numpy object formatted as string and it contains the data form voice.
'''

class FrameData:
    __numpy_data = object
    __esp_id = object
    __offset: object

    def __init__(self, numpy_data, esp_id, offset):
        self.numpy_data = numpy_data
        self.esp_id = esp_id
        self.offset = offset

    @property
    def numpy_data(self):
        return self.__numpy_data

    @numpy_data.setter
    def numpy_data(self, val):
        self.__numpy_data = val

    @property
    def esp_id(self):
        return self.__esp_id

    @esp_id.setter
    def esp_id(self, val):
        self.__esp_id = val

    @property
    def offset(self):
        return self.__offset

    @offset.setter
    def offset(self, val):
        self.__offset = val
