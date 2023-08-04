""" Microwave oven models"""
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from src.backend.config import get_settings


class MicrowaveStates(str, Enum):
    """Microwave oven states"""

    ON = "On"
    OFF = "Off"


class MicrowaveInfoModel(BaseModel):
    """Microwave oven parameters model"""

    microwave_id: str
    state: str = MicrowaveStates.OFF
    power: int = Field(
        default_factory=lambda: str(get_settings().DEFAULT_MICROWAVE_MIN_POWER)
    )
    counter: int = Field(
        default_factory=lambda: str(get_settings().DEFAULT_MICROWAVE_MIN_COUNTER)
    )


class MicrowaveAdjustmentModel(BaseModel):
    """Microwave oven adjustments model"""

    power_step: Optional[int] = Field(
        default=None, gt=-101, lt=101, title="Power percentage increase/decrease step"
    )
    counter_step: Optional[int] = Field(
        default=None, gt=-101, lt=101, title="Counter increase/decrease step"
    )
