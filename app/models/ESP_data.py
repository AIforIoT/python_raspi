
'''
This object contains all the relevant information about an ESP.
'''

class ESP_data:
    __esp_id = object
    __esp_ip = object
    __x = object
    __y = object
    __type = object
    __side = object
    __location = object

    def __init__(self, esp_id, esp_ip, x, y, type, side, location):
        self.__esp_id = esp_id
        self.__esp_ip = esp_ip
        self.__x = x
        self.__y = y
        self.__type = type
        self.__side = side
        self.__location = location


    @property
    def esp_id(self):
        return self.__esp_id

    @esp_id.setter
    def esp_id(self, val):
        self.__esp_id = val

    @property
    def esp_ip(self):
        return self.__esp_ip

    @esp_ip.setter
    def esp_ip(self, val):
        self.__esp_ip = val

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, val):
        self.__x = val

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, val):
        self.__y = val

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, val):
        self.__type = val


    @property
    def side(self):
        return self.__side

    @side.setter
    def side(self, val):
        self.__side = val

    @property
    def location(self):
        return self.__location

    @location.setter
    def location(self, val):
        self.__location = val