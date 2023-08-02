""" Microwave Oven API endpoints """
import json
from typing import Optional

from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException, status

from src.backend.api.utils.management import MicrowaveCounter
from src.backend.api.utils.microwaves import counter_adjustment, power_adjustment
from src.backend.crud.db import db_client
from src.backend.models.microwaves import (
    MicrowaveInfoModel,
    MicrowaveAdjustmentModel,
)
from src.backend.services.authentication import authenticate_user

START_UP_DELAY = 1

router = APIRouter(prefix="/microwaves", tags=["Microwaves"])


@router.get("/{microwave_id}/", response_model=Optional[MicrowaveInfoModel])
async def get_microwave_state(
    microwave_id: str,
) -> Optional[MicrowaveInfoModel]:
    """
    Get specified microwave oven
    Args:
        microwave_id: microwave db id

    Returns:
        MicrowaveInfoModel object if object found
    """
    obj = db_client().get_item(microwave_id)
    return MicrowaveInfoModel(**json.loads(obj)) if obj else None


@router.patch(
    "/{microwave_id}/adjustment",
)
async def microwave_oven_adjustment(
    microwave_id: str,
    adjustments: MicrowaveAdjustmentModel,
    background_tasks: BackgroundTasks,
) -> MicrowaveInfoModel:
    """
    Microwave Oven adjustment
    Args:
        microwave_id: microwave oven db id
        adjustments: microwave adjustment parameters with values
        background_tasks: background task for countdown

    Returns:
        MicrowaveInfoModel object
    """
    try:
        obj = db_client().get_item(microwave_id)
        microwave_obj = MicrowaveInfoModel(**json.loads(obj))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Microwave Object ({microwave_id}) Not Found",
        ) from None

    if adjustments.counter_step:
        microwave_obj = counter_adjustment(
            microwave_id, microwave_obj, adjustments, background_tasks
        )
    if adjustments.power_step:
        microwave_obj = power_adjustment(microwave_id, microwave_obj, adjustments)
    return microwave_obj


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
        String info
    """
    try:
        MicrowaveCounter(microwave_id=microwave_id).stop_task()
        db_client_connection = db_client()
        obj = db_client_connection.get_item(microwave_id)
        if obj:
            db_client_connection.create_item(
                microwave_id,
                MicrowaveInfoModel(microwave_id=microwave_id).model_dump_json(),
            )
            db_client_connection.execute_transaction()
            return f"Hi {user}, microwave oven ({microwave_id}) canceled"
        return f"Hi {user}, microwave oven ({microwave_id}) not found"
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to cancel {microwave_id}",
        ) from None
