

class Volume_data:
    __esp_id = object
    __timestamp = object
    __delay = object
    __volume = object

    def __init__(self, esp_id, timestamp, delay, volume):
        self.__esp_id = esp_id
        self.__timestamp = timestamp
        self.__delay = delay
        self.__volume = volume


    @property
    def esp_id(self):
        return self.__esp_id

    @esp_id.setter
    def esp_id(self, val):
        self.__esp_id = val

    @property
    def timestamp(self):
        return self.__timestamp

    @timestamp.setter
    def timestamp(self, val):
        self.__timestamp = val

    @property
    def delay(self):
        return self.__delay

    @delay.setter
    def delay(self, val):
        self.__delay = val

    @property
    def volume(self):
        return self.__volume

    @volume.setter
    def volume(self, val):
        self.__volume = val
