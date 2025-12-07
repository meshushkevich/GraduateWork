from dataclasses import dataclass
from enum import Enum


@dataclass
class MCU:
    class MCU_Type(Enum):
        REAL = "REAL"
        FAKE = "FAKE"

    class MCU_ConnectionType(Enum):
        USB = "USB"

    id: int
    name: str
    description: str

    type: MCU_Type
    connection_type: MCU_ConnectionType
    is_connected: bool
    dev_id: int
