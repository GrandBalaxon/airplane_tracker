from unittest.mock import patch, MagicMock

import pytest

from src.api import AirplanesAPI


@patch("requests.get")
def test_make_request_success(mock_get):
    """Тест успешного HTTP-запроса."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"key": "value"}

    mock_get.return_value = mock_response

    result = AirplanesAPI._make_request("http://test.com")

    assert result == {"key": "value"}


@patch("requests.get")
def test_make_request_failure(mock_get):
    """Тест ошибки при плохом статус-коде."""
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.text = "Server error"

    mock_get.return_value = mock_response

    with pytest.raises(Exception):
        AirplanesAPI._make_request("http://test.com")

@patch("src.api.AirplanesAPI._make_request")
def test_get_country_bbox_success(mock_request):
    """Тест получения bounding box."""
    mock_request.return_value = [
        {"boundingbox": ["1", "2", "3", "4"]}
    ]

    api = AirplanesAPI()
    bbox = api._get_country_bbox("Uzbekistan")

    assert bbox == ["1", "2", "3", "4"]


@patch("src.api.AirplanesAPI._make_request")
def test_get_country_bbox_empty(mock_request):
    """Тест ошибки при пустом bbox."""
    mock_request.return_value = []
    api = AirplanesAPI()

    with pytest.raises(
            ValueError,
            match="Некорректно указанная страна - Nowhere, полученная bbox пуста."
    ):
        api._get_country_bbox("Nowhere")


@patch("src.api.AirplanesAPI._make_request")
def test_get_airplanes_states(mock_request):
    """Тест получения состояний самолётов."""
    mock_request.return_value = {"states": []}

    api = AirplanesAPI()
    result = api._get_airplanes_states(["1", "2", "3", "4"])

    assert isinstance(result, dict)


@patch("src.api.AirplanesAPI._get_airplanes_states")
@patch("src.api.AirplanesAPI._get_country_bbox")
def test_get_airplanes_success(mock_bbox, mock_states):
    """Тест полного получения самолётов."""
    mock_bbox.return_value = ["1", "2", "3", "4"]
    mock_states.return_value = {
        "states": [["plane1"], ["plane2"]]
    }

    api = AirplanesAPI()
    result = api.get_airplanes("Uzbekistan")

    assert len(result) == 2


@patch("src.api.AirplanesAPI._get_airplanes_states")
@patch("src.api.AirplanesAPI._get_country_bbox")
def test_get_airplanes_empty(mock_bbox, mock_states):
    """Тест случая без самолётов."""
    mock_bbox.return_value = ["1", "2", "3", "4"]
    mock_states.return_value = {}

    api = AirplanesAPI()
    result = api.get_airplanes("Uzbekistan")

    assert result == []
