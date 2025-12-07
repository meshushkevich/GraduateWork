from dataclasses import dataclass
from enum import Enum

from pydantic import BaseModel, Field


@dataclass
class MCU:
    class MCU_Type(Enum):
        REAL = "REAL"
        FAKE = "FAKE"

    class MCU_ConnectionType(Enum):
        USB = "USB"

    name: str = Field(description="Name of the MCU")
    description: str = Field(description="Description of the MCU")

    type: MCU_Type = Field(default=MCU_Type.FAKE)
    connection_type: MCU_ConnectionType = Field(default=MCU_ConnectionType.USB)
    is_connected: bool = Field(default=True)
    dev_id: int = Field(default=0)
