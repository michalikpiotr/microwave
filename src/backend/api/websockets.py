import asyncio
import json

from fastapi import APIRouter, WebSocket

from src.backend.crud.db import db_client
from src.backend.models.microwaves import DEFAULT_MICROWAVE_ID

router = APIRouter()


@router.websocket("/ws_pull/")
async def websocket_endpoint(websocket: WebSocket):
    """
    Connection for getting current state of Microwave Oven
    Args:
        websocket: WebSocket object
    """
    await websocket.accept()

    while True:
        obj = db_client().get_item(DEFAULT_MICROWAVE_ID)
        await websocket.send_json(json.loads(obj))

        await asyncio.sleep(1)
