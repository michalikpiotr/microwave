""" Websockets """
import asyncio
import json

from fastapi import APIRouter, WebSocket

from src.backend.config import get_settings
from src.backend.crud.db import db_client

router = APIRouter()


@router.websocket("/ws_pull/")
async def websocket_endpoint(websocket: WebSocket):
    """
    Connection for getting current state of Microwave Oven
    Args:
        websocket: WebSocket object
    """
    settings = get_settings()
    await websocket.accept()

    while True:
        obj = db_client().get_item(settings.DEFAULT_MICROWAVE_ID)
        await websocket.send_json(json.loads(obj))

        await asyncio.sleep(1)
