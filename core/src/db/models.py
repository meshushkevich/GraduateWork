from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class MCUs_Table(Base):
    __tablename__ = "mcus"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)


class Collectors_Table(Base):
    __tablename__ = "collectors"

    id = Column(Integer, primary_key=True)
    fingerprint = Column(String(255), nullable=False)


class Sensors_Table(Base):
    __tablename__ = "sensors"

    id = Column(Integer, primary_key=True)
    mcu_id = Column(Integer, ForeignKey("mcus.id"), nullable=False)
    name = Column(String(255), nullable=False)


class History_Table(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True)
    collector_id = Column(Integer, ForeignKey("collectors.id"), nullable=False)
    mcu_id = Column(Integer, ForeignKey("mcus.id"), nullable=False)
    sensor_id = Column(Integer, ForeignKey("sensors.id"), nullable=False)
    value = Column(Float(16), nullable=False)
    timestamp = Column(DateTime(), nullable=False)
