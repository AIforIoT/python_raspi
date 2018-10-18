import os

class ConfigParams:
    __esp_id: object
    __frame_id: object
    __delay: object
    __power: object
    __offset: object

    def __init__(self, esp_id, frame_id, delay, power, offset):
        self.esp_id = esp_id
        self.frame_id = frame_id
        self.delay = delay
        self.power = power
        self.offset = offset


    @property
    def esp_id(self):
        return self.__esp_id

    @esp_id.setter
    def esp_id(self, val):
        self.__esp_id = val

    @property
    def frame_id(self):
        return self.__frame_id

    @frame_id.setter
    def frame_id(self, val):
        self.__frame_id = val

    @property
    def delay(self):
        return self.__delay

    @delay.setter
    def delay(self, val):
        self.__delay = val

    @property
    def power(self):
        return self.__power

    @power.setter
    def power(self, val):
        self.__power = val

    @property
    def offset(self):
        return self.__offset

    @offset.setter
    def offset(self, val):
        self.__offset = val

class FrameData:
    __numpy_data = object
    __config_params = object

    def __init__(self, numpy_data, esp_id, frame_id, delay, power, offset):
        self.numpy_data = numpy_data
        self.config_params = ConfigParams(esp_id, frame_id, delay, power, offset)


    @property
    def numpy_data(self):
        return self.__numpy_data

    @numpy_data.setter
    def numpy_data(self, val):
        self.__numpy_data = val

    @property
    def config_params(self):
        return self.__config_params

    @config_params.setter
    def config_params(self, val):
        self.__config_params = val


