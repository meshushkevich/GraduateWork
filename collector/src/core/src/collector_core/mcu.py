from enum import Enum

from pydantic import BaseModel, Field


class MCU(BaseModel):
    class MCU_Type(Enum):
        REAL = "REAL"
        FAKE = "FAKE"

    class MCU_ConnectionType(Enum):
        USB = "USB"

    dev_id: int = Field(default=0)
    description: str = Field(description="Description of the MCU")

    type: MCU_Type = Field(default=MCU_Type.FAKE)
    connection_type: MCU_ConnectionType = Field(default=MCU_ConnectionType.USB)
    is_connected: bool = Field(default=True)
