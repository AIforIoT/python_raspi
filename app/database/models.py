from sqlalchemy import Column, Integer, String
from app.database.database import Base
from app.models.data_request_object import FrameData


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