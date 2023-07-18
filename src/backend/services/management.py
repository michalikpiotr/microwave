import asyncio
import json

from src.backend.crud.db import db_client
from src.backend.models.microwaves import (
    MicrowaveInfoModel,
    MicrowaveStates,
    DEFAULT_MICROWAVE_MIN_COUNTER,
    DEFAULT_MICROWAVE_MIN_POWER,
)


class MicrowaveCounter:
    """Microwave Oven shared counter"""

    _instance = None
    _count = 0

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def increment(cls, count):
        cls._count += count

    @classmethod
    def get_count(cls):
        return cls._count

    @classmethod
    def stop_task(cls):
        cls._count = 0

    @classmethod
    async def decrement_counter(cls, microwave_obj: MicrowaveInfoModel):
        db_client_connection = db_client()
        while cls._count > 0:
            cls._count -= 1
            await asyncio.sleep(1)
            obj = db_client_connection.get_item(microwave_obj.microwave_id)
            microwave_obj = MicrowaveInfoModel(**json.loads(obj))
            microwave_obj.counter = cls._count
            microwave_obj.state = MicrowaveStates.on
            db_client_connection.create_item(
                microwave_obj.microwave_id, microwave_obj.model_dump_json()
            )
        if (
            microwave_obj.counter == DEFAULT_MICROWAVE_MIN_COUNTER
            and microwave_obj.power == DEFAULT_MICROWAVE_MIN_POWER
        ):
            microwave_obj.state = MicrowaveStates.off
        db_client_connection.create_item(
            microwave_obj.microwave_id, microwave_obj.model_dump_json()
        )
