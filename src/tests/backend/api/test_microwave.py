""" Test microwave oven api """
import os
from unittest.mock import patch

from fastapi.testclient import TestClient
from pytest import mark
from starlette import status

from src.backend.models.microwaves import MicrowaveInfoModel


class DB:
    """DB class"""

    def get_item(self):
        """Get db item"""
        return b'{"microwave_id":"test1","state":"Off","power":0,"counter":0}'


def test_microwave_get(client: TestClient):
    """Microwave oven get microwave by id"""
    microwave_id = os.environ["DEFAULT_MICROWAVE_ID_1"]

    with patch("src.backend.api.microwaves.db_client", return_value=DB):
        response = client.get(f"/microwaves/{microwave_id}/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "counter": 0,
        "microwave_id": microwave_id,
        "power": 0,
        "state": "Off",
    }, response.json()


def test_microwave_power_adjustment(client: TestClient):
    """Microwave oven adjustment"""
    microwave_id = os.environ["DEFAULT_MICROWAVE_ID_1"]
    power_step = 10
    microwave_db_new_obj = MicrowaveInfoModel(
        microwave_id=f"{microwave_id}", state="On", power=power_step, counter=0
    )
    request_body: dict[str, int] = {
        "power_step": power_step,
    }

    with patch("src.backend.api.microwaves.db_client", return_value=DB):
        with patch(
            "src.backend.api.microwaves.power_adjustment",
            return_value=microwave_db_new_obj,
        ):
            response = client.patch(
                f"/microwaves/{microwave_id}/adjustment", json=request_body
            )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "counter": 0,
        "microwave_id": f"{microwave_id}",
        "power": power_step,
        "state": "On",
    }, response.json()


def test_microwave_counter_adjustment(client: TestClient):
    """Microwave oven adjustment"""
    microwave_id = os.environ["DEFAULT_MICROWAVE_ID_1"]
    counter_step = 10
    microwave_db_new_obj = MicrowaveInfoModel(
        microwave_id=f"{microwave_id}", state="On", power=0, counter=counter_step
    )
    request_body: dict[str, int] = {
        "counter_step": counter_step,
    }

    with patch("src.backend.api.microwaves.db_client", return_value=DB):
        with patch(
            "src.backend.api.microwaves.counter_adjustment",
            return_value=microwave_db_new_obj,
        ):
            response = client.patch(
                f"/microwaves/{microwave_id}/adjustment", json=request_body
            )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "counter": counter_step,
        "microwave_id": f"{microwave_id}",
        "power": 0,
        "state": "On",
    }, response.json()


@mark.parametrize(
    "counter_step,error_msg",
    [
        [101, "Input should be less than 101"],
        [-101, "Input should be greater than -101"],
    ],
)
def test_microwave_invalid_counter_adjustment(
    counter_step, error_msg, client: TestClient
):
    """Microwave oven adjustment"""
    microwave_id = os.environ["DEFAULT_MICROWAVE_ID_1"]
    microwave_db_new_obj = MicrowaveInfoModel(
        microwave_id=f"{microwave_id}", state="On", power=0, counter=counter_step
    )
    request_body: dict[str, int] = {
        "counter_step": counter_step,
    }

    with patch("src.backend.api.microwaves.db_client", return_value=DB):
        with patch(
            "src.backend.api.microwaves.power_adjustment",
            return_value=microwave_db_new_obj,
        ):
            response = client.patch(
                f"/microwaves/{microwave_id}/adjustment", json=request_body
            )
    assert response.json()["detail"][0]["msg"] == error_msg
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@mark.parametrize(
    "power_step,error_msg",
    [
        [101, "Input should be less than 101"],
        [-101, "Input should be greater than -101"],
    ],
)
def test_microwave_invalid_power_adjustment(power_step, error_msg, client: TestClient):
    """Microwave oven adjustment"""
    microwave_id = os.environ["DEFAULT_MICROWAVE_ID_1"]
    microwave_db_new_obj = MicrowaveInfoModel(
        microwave_id=f"{microwave_id}", state="On", power=0, counter=power_step
    )
    request_body: dict[str, int] = {
        "counter_step": power_step,
    }

    with patch("src.backend.api.microwaves.db_client", return_value=DB):
        with patch(
            "src.backend.api.microwaves.counter_adjustment",
            return_value=microwave_db_new_obj,
        ):
            response = client.patch(
                f"/microwaves/{microwave_id}/adjustment", json=request_body
            )
    assert response.json()["detail"][0]["msg"] == error_msg
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
