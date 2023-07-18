from enum import Enum

from fastapi import Query
from pydantic import BaseModel

DEFAULT_MICROWAVE_ID: str = "microwave_1"
DEFAULT_MICROWAVE_MAX_POWER: int = 1500
DEFAULT_MICROWAVE_MIN_POWER: int = 0
DEFAULT_MICROWAVE_MAX_COUNTER: int = 900
DEFAULT_MICROWAVE_MIN_COUNTER: int = 0


class MicrowaveStates(str, Enum):
    """Microwave oven states"""

    on = "On"
    off = "Off"


class MicrowaveInfoModel(BaseModel):
    """Microwave oven parameters"""

    microwave_id: str = DEFAULT_MICROWAVE_ID
    state: str = MicrowaveStates.off
    power: int = DEFAULT_MICROWAVE_MIN_POWER
    counter: int = DEFAULT_MICROWAVE_MIN_COUNTER


class MicrowavePowerChangeModel(BaseModel):
    """Microwave oven power change model with limitations"""

    change: float = Query(default=0.1, gt=-1, lt=1)


class MicrowaveCounterChangeModel(BaseModel):
    """Microwave oven counter change model with limitations"""

    change: int = Query(default=10, gt=-200, lt=200)
