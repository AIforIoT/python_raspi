from sqlalchemy import Column, Integer, String
from app.database.database import Base
from app.models.data_request_object import FrameData
from app.models.ESP_data import ESP_data
from app.models.volume_data import Volume_data


class SQLFrame(Base):
    __tablename__ = 'frame_data'
    id = Column(Integer, primary_key=True)
    esp_id = Column(String(50), unique=True)
    delay = Column(String(50))
    power = Column(String(50))
    offset = Column(String(50))
    timestamp = Column(String(50))
    numpy_data = Column(String(9000))

    def __init__(self, esp_id=None, delay=None, power=None, offset=None, timestamp=None, numpy_data=None):
        self.esp_id = esp_id
        self.delay = delay
        self.power = power
        self.offset = offset
        self.timestamp = timestamp
        self.numpy_data = numpy_data

    def __repr__(self):
        return FrameData(self.numpy_data, self.esp_id, self.delay, self.power, self.offset, self.timestamp)


class ESPdata(Base):
    __tablename__ = 'esp_data'
    id = Column(Integer, primary_key=True)
    esp_id = Column(String(50), unique=True)
    esp_ip = Column(String(50), unique=True)
    x = Column(String(50), nullable=False)
    y = Column(String(50), nullable=False)
    type = Column(String(50), nullable=False)
    side = Column(String(50), nullable=False)
    location = Column(String(50), nullable=False)

    def __init__(self, esp_id=None, esp_ip=None, x=None, y=None, type=None, side=None, location=None):
        self.esp_id = esp_id
        self.esp_ip = esp_ip
        self.x = x
        self.y = y
        self.type = type
        self.side = side
        self.location = location

    def __repr__(self):
        return ESP_data(self.esp_id, self.esp_ip, self.x, self.y, self.type, self.side, self.location)
    
class VOLUMEdata(Base):
    __tablename__ = 'volume_data'
    id = Column(Integer, primary_key=True)
    esp_id = Column(String(50), unique=False)
    timestamp = Column(String(50))
    delay = Column(String(50))
    volume = Column(String(50))
    
    def __init__(self, esp_id=None, timestamp=0, delay=0, volume=0):
        self.esp_id = esp_id
        self.volume = volume
        self.delay = delay
        self.timestamp = timestamp
    
    def __repr__(self):
        return Volume_data(self.esp_id, self.timestamp, self.delay, self.volume)