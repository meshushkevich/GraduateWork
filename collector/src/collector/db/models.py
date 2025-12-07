from sqlalchemy import Boolean, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

from collector.mcu import MCU

Base = declarative_base()


class MCU_Table(Base):
    __tablename__ = "mcus"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    type = Column(MCU.MCU_Type, nullable=False)
    connection_type = Column(MCU.MCU_ConnectionType, nullable=False)
    is_connected = Column(Boolean, default=False)
    dev_id = Column(Integer, nullable=False)
