
class ESP_data:
    __esp_id = object
    __x = object
    __y = object
    __type = object

    def __init__(self, esp_id, x, y, type):
        self.__esp_id = esp_id
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

