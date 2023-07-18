from fastapi import APIRouter

from src.backend.crud.db import db_client
from src.backend.models.microwaves import (
    MicrowaveInfoModel,
    MicrowaveStates,
    DEFAULT_MICROWAVE_MIN_POWER,
    DEFAULT_MICROWAVE_MIN_COUNTER,
    DEFAULT_MICROWAVE_ID,
)

router = APIRouter()


@router.on_event("startup")
async def startup():
    """Data upload to db client on app startup"""
    default_microwave = MicrowaveInfoModel(
        state=MicrowaveStates.off,
        power=DEFAULT_MICROWAVE_MIN_POWER,
        counter=DEFAULT_MICROWAVE_MIN_COUNTER,
    )

    db_client().create_item(DEFAULT_MICROWAVE_ID, default_microwave.model_dump_json())
