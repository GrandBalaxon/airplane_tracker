import pytest
from unittest.mock import patch, MagicMock

from src.base_api import BaseAPIClient


class DummyAPI(BaseAPIClient):
    def get_airplanes(self, country: str):
        return []


@patch("requests.get")
def test_make_request_success(mock_get):
    """Тест успешного HTTP-запроса."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"key": "value"}

    mock_get.return_value = mock_response

    result = DummyAPI._make_request("http://test.com")

    assert result == {"key": "value"}


@patch("requests.get")
def test_make_request_failure(mock_get):
    """Тест ошибки при плохом статус-коде."""
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.text = "Server error"

    mock_get.return_value = mock_response

    with pytest.raises(Exception):
        DummyAPI._make_request("http://test.com")
