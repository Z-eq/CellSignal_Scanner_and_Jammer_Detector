from sqlalchemy import Column, Integer, String, DateTime, Float
from app import db

class WifiData(db.Model):
    __tablename__ = 'wifi_scans'

    id = Column(Integer, primary_key=True)
    ssid = Column(String(50))
    address = Column(String(50))
    rssi = Column(Integer)
    timestamp = Column(DateTime)

class JammingEvent(db.Model):
    __tablename__ = 'jamming_events'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    current_strength = Column(Float)
    moving_avg = Column(Float)
    packet_loss_avg = Column(Float)

class Watchlist(db.Model):
    __tablename__ = 'watchlist'

    id = Column(Integer, primary_key=True)
    ssid = Column(String(50))
    address = Column(String(50))

