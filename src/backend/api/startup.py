""" App startup operations """
from fastapi import APIRouter

from src.backend.config import (
    get_settings,
)
from src.backend.crud.db import db_client
from src.backend.models.microwaves import MicrowaveInfoModel, MicrowaveStates

router = APIRouter()


@router.on_event("startup")
async def startup():
    """Data upload to db client on app startup"""
    settings = get_settings()
    default_microwave = MicrowaveInfoModel(
        state=MicrowaveStates.OFF,
        power=settings.DEFAULT_MICROWAVE_MIN_POWER,
        counter=settings.DEFAULT_MICROWAVE_MIN_COUNTER,
    )

    db_client().create_item(
        settings.DEFAULT_MICROWAVE_ID, default_microwave.model_dump_json()
    )
