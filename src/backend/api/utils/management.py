""" Microwave oven management"""
import asyncio
import enum
import json

from src.backend.config import get_settings
from src.backend.crud.redis import RedisTransaction
from src.backend.models.microwaves import (
    MicrowaveInfoModel,
    MicrowaveStates,
)


class MicrowaveDetails(enum.Enum):
    """Microwave instance details"""

    INSTANCE_ID = enum.auto()
    COUNT = enum.auto()


class MicrowaveCounter:
    """Microwave Oven shared background counter"""

    _instances = {}

    def __new__(cls, db_client_connection, microwave_id: str):
        if microwave_id not in cls._instances:
            cls._instances[microwave_id] = {
                MicrowaveDetails.INSTANCE_ID: super().__new__(cls),
                MicrowaveDetails.COUNT: 0,
            }
        return cls._instances[microwave_id][MicrowaveDetails.INSTANCE_ID]

    def __init__(self, db_client_connection, microwave_id):
        self._db_client_connection = db_client_connection
        self._microwave_id = microwave_id

    def increment(self, count):
        """Microwave oven counter incrementation"""
        self._instances[self._microwave_id][MicrowaveDetails.COUNT] += count

    def get_count(self):
        """Get microwave oven current counter"""
        return self._instances[self._microwave_id][MicrowaveDetails.COUNT]

    def stop_task(self):
        """Set counter to 0 to stop the microwave oven"""
        self._instances[self._microwave_id][MicrowaveDetails.COUNT] = 0

    async def decrement_counter(self, microwave_obj: MicrowaveInfoModel):
        """Microwave oven countdown"""

        while self._instances[self._microwave_id][MicrowaveDetails.COUNT] > 0:
            with RedisTransaction(self._db_client_connection) as transaction:
                self._instances[self._microwave_id][MicrowaveDetails.COUNT] -= 1
                await asyncio.sleep(1)

                obj = self._db_client_connection.get_item(microwave_obj.microwave_id)
                microwave_obj = MicrowaveInfoModel(**json.loads(obj))
                microwave_obj.counter = self._instances[self._microwave_id][
                    MicrowaveDetails.COUNT
                ]
                microwave_obj.state = MicrowaveStates.ON
                transaction.create_item(
                    microwave_obj.microwave_id, microwave_obj.model_dump_json()
                )

        MicrowaveCounter.microwave_off_check(microwave_obj, self._db_client_connection)

    @classmethod
    def microwave_off_check(cls, microwave_obj, db_client_connection):
        """Function to set the state of the microwave oven to Off when conditions are met"""

        settings = get_settings()
        if (
            microwave_obj.counter == settings.DEFAULT_MICROWAVE_MIN_COUNTER
            and microwave_obj.power == settings.DEFAULT_MICROWAVE_MIN_POWER
        ):
            microwave_obj.state = MicrowaveStates.OFF
            with RedisTransaction(db_client_connection) as transaction:
                transaction.create_item(
                    microwave_obj.microwave_id, microwave_obj.model_dump_json()
                )
