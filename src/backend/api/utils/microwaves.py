""" Microwave oven available operations """

from fastapi import BackgroundTasks, HTTPException, status

from src.backend.api.utils.management import MicrowaveCounter
from src.backend.config import get_settings
from src.backend.crud.db import db_client
from src.backend.models.microwaves import (
    MicrowaveStates,
    MicrowaveInfoModel,
    MicrowaveAdjustmentModel,
)

START_UP_DELAY = 1


def counter_adjustment(
    microwave_id: str,
    microwave_obj: MicrowaveInfoModel,
    adjustments: MicrowaveAdjustmentModel,
    background_tasks: BackgroundTasks,
) -> MicrowaveInfoModel:
    """
    Microwave oven counter adjustment

    Args:
        microwave_id: microwave oven db id
        microwave_obj: microwave oven MicrowaveInfoModel object
        adjustments: microwave oven adjustments model
        background_tasks: background task for countdown

    Returns:
        microwave oven MicrowaveInfoModel object
    """
    settings = get_settings()
    try:
        if (
            settings.DEFAULT_MICROWAVE_MIN_COUNTER
            < microwave_obj.counter + adjustments.counter_step
            <= settings.DEFAULT_MICROWAVE_MAX_COUNTER
        ):
            counter_obj = MicrowaveCounter(microwave_id=microwave_id)

            increment_value = adjustments.counter_step + START_UP_DELAY
            microwave_obj.counter += increment_value
            if counter_obj.get_count() == settings.DEFAULT_MICROWAVE_MIN_COUNTER:
                counter_obj.increment(increment_value)
                background_tasks.add_task(counter_obj.decrement_counter, microwave_obj)
                del counter_obj
            else:
                counter_obj.increment(increment_value)
        return microwave_obj
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to change counter of {microwave_id}",
        ) from None


def power_adjustment(
    microwave_id: str,
    microwave_obj: MicrowaveInfoModel,
    adjustments: MicrowaveAdjustmentModel,
) -> MicrowaveInfoModel:
    """
    Microwave oven power adjustment

    Args:
        microwave_id: microwave oven db id
        microwave_obj: microwave oven MicrowaveInfoModel object
        adjustments: microwave oven adjustments model

    Returns:
        microwave oven MicrowaveInfoModel object
    """
    settings = get_settings()
    try:
        power_step = (
            adjustments.power_step * settings.DEFAULT_MICROWAVE_MAX_POWER * 0.01
        )
        if (
            settings.DEFAULT_MICROWAVE_MIN_POWER
            <= microwave_obj.power + power_step
            <= settings.DEFAULT_MICROWAVE_MAX_POWER
        ):
            microwave_obj.power += power_step
            microwave_obj.state = (
                MicrowaveStates.ON
                if microwave_obj.power > 0 or microwave_obj.counter > 0
                else MicrowaveStates.OFF
            )

        db_client().create_item(microwave_id, microwave_obj.model_dump_json())
        return microwave_obj
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to change power of {microwave_id}",
        ) from None
