import json
from typing import Optional, Union

from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException, status

from src.backend.crud.db import db_client
from src.backend.models.microwaves import (
    MicrowaveInfoModel,
    MicrowaveCounterChangeModel,
    MicrowaveStates,
    MicrowavePowerChangeModel,
    DEFAULT_MICROWAVE_MAX_POWER,
    DEFAULT_MICROWAVE_MIN_POWER,
    DEFAULT_MICROWAVE_MIN_COUNTER,
    DEFAULT_MICROWAVE_MAX_COUNTER,
)
from src.backend.services.authentication import authenticate_user
from src.backend.services.management import MicrowaveCounter

START_UP_DELAY = 1

router = APIRouter(prefix="/microwaves", tags=["Microwaves"])


@router.get("/{microwave_id}/", response_model=Optional[MicrowaveInfoModel])
async def get_microwave_state(
    microwave_id: str,
) -> MicrowaveInfoModel:
    obj = db_client().get_item(microwave_id)
    return MicrowaveInfoModel(**json.loads(obj)) if obj else None


@router.post(
    "/{microwave_id}/power_adjustment",
)
async def power_adjustment(
    microwave_id: str,
    microwave: MicrowavePowerChangeModel,
) -> MicrowaveInfoModel:
    """
    Changing power of Microwave Oven
    Args:
        microwave_id: microwave oven db id
        microwave: microwave parameters

    Returns:
        MicrowaveInfoModel object
    """
    try:
        obj = db_client().get_item(microwave_id)
        microwave_obj = MicrowaveInfoModel(**json.loads(obj))
        power_step = microwave.change * DEFAULT_MICROWAVE_MAX_POWER
        if (
            DEFAULT_MICROWAVE_MIN_POWER
            <= microwave_obj.power + power_step
            <= DEFAULT_MICROWAVE_MAX_POWER
        ):
            microwave_obj.power += power_step
            microwave_obj.state = (
                MicrowaveStates.on
                if microwave_obj.power > 0 or microwave_obj.counter > 0
                else MicrowaveStates.off
            )

        db_client().create_item(microwave_id, microwave_obj.model_dump_json())
        return microwave_obj
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to change power of {microwave_id}",
        ) from None


@router.post(
    "/{microwave_id}/counter_adjustment",
)
async def counter_adjustment(
    microwave_id: str,
    microwave: MicrowaveCounterChangeModel,
    background_tasks: BackgroundTasks,
) -> Union[MicrowaveInfoModel, str]:
    """
    Changing counter of Microwave Oven
    Args:
        microwave_id: microwave oven db id
        microwave: microwave parameters
        background_tasks: background task for count down

    Returns:
        MicrowaveInfoModel object or string communicate
    """
    try:
        obj = db_client().get_item(microwave_id)
        microwave_obj = MicrowaveInfoModel(**json.loads(obj))
        if (
            DEFAULT_MICROWAVE_MIN_COUNTER
            < microwave_obj.counter + microwave.change
            <= DEFAULT_MICROWAVE_MAX_COUNTER
        ):
            counter_obj = MicrowaveCounter()
            if MicrowaveCounter.get_count() == DEFAULT_MICROWAVE_MIN_COUNTER:
                counter_obj.increment(microwave.change + START_UP_DELAY)
                background_tasks.add_task(counter_obj.decrement_counter, microwave_obj)
                del counter_obj
            else:
                counter_obj.increment(microwave.change + START_UP_DELAY)
            return microwave_obj
        else:
            return f"Counter not changed, range: {DEFAULT_MICROWAVE_MIN_COUNTER}s - {DEFAULT_MICROWAVE_MAX_COUNTER}s"
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to change counter of {microwave_id}",
        ) from None


@router.post("/{microwave_id}/cancel")
async def cancel(
    microwave_id: str,
    user: dict = Depends(authenticate_user),
) -> str:
    """
    Cancel Microwave Oven job by authenticated user
    Args:
        microwave_id: microwave oven db id
        user: logged user

    Returns:
        String communicate
    """
    try:
        MicrowaveCounter().stop_task()

        db_client().create_item(microwave_id, MicrowaveInfoModel().model_dump_json())

        return f"Hi {user}, microwave oven ({microwave_id}) canceled"
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to cancel {microwave_id}",
        ) from None
