
class ESP_data:
    __esp_id = object
    __esp_ip = object
    __x = object
    __y = object
    __type = object

    def __init__(self, esp_id, esp_ip, x, y, type):
        self.__esp_id = esp_id
        self.__esp_ip = esp_ip
        self.__x = x
        self.__y = y
        self.__type = type


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

    @x.setter
    def y(self, val):
        self.__y = val

    @property
    def type(self):
        return self.__type

    @x.setter
    def type(self, val):
        self.__type = val

