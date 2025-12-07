from dataclasses import dataclass

from sqlalchemy import Enum


@dataclass
class MCU:
    class MCU_Type(Enum):
        REAL = "Real"
        FAKE = "Fake"

    class MCU_ConnectionType(Enum):
        USB = "USB"

    id: int
    name: str
    description: str

    type: MCU_Type
    connection_type: MCU_ConnectionType
    is_connected: bool
    dev_id: int
