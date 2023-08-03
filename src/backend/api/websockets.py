""" Websockets """
import asyncio
import json

from fastapi import APIRouter, WebSocket

from src.backend.config import get_settings
from src.backend.crud.redis import RedisCrud

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

    with RedisCrud() as db_client_connection:
        while True:
            obj = db_client_connection.get_item(settings.DEFAULT_MICROWAVE_ID_1)
            await websocket.send_json(json.loads(obj))
            await asyncio.sleep(1)
