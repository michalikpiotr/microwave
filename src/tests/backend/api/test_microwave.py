from unittest.mock import patch

from fastapi.testclient import TestClient
from starlette import status


def test_microwave_get(client: TestClient):
    """Microwave oven get microwave by id"""
    microwave_id = "test1"
    microwave_db_obj = b'{"microwave_id":"test1","state":"Off","power":0,"counter":0}'

    with patch(
        "src.backend.api.microwaves.db_client.get_item", return_value=microwave_db_obj
    ):
        response = client.get(f"/microwaves/{microwave_id}/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "counter": 0,
        "microwave_id": "test1",
        "power": 0,
        "state": "Off",
    }, response.json()
