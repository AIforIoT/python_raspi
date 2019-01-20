
class outputMessage:

    __iouti = object
    __status = object
    __location = object
    __typeObj = object

    def __init__(self, iouti, status, location, typeObj):
        self.iouti = iouti
        self.status = status
        self.location = location
        self.typeObj = typeObj

    @property
    def iouti(self):
        return self.__iouti

    @iouti.setter
    def iouti(self, val):
        self.__iouti = val

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, val):
        self.__status = val

    @property
    def location(self):
        return self.__location

    @location.setter
    def location(self, val):
        self.__location = val

    @property
    def typeObj(self):
        return self.__typeObj

    @typeObj.setter
    def typeObj(self, val):
        self.__typeObj = val
