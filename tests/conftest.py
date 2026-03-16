import pytest

from src.airplane import Airplane


@pytest.fixture
def sample_airplanes_data():
    """Пример данных самолётов для тестов."""
    list_ = [
        Airplane("uwu1", "Uzbekistan", False, 200.0, 2000.0),
        Airplane("uwu2", "Uzbekistan", False, 200.0, 1000.0),
        Airplane("uwu3", "Uzbekistan", False, 200.0, 2000.0),
        Airplane("uwu4", "Uzbekistan", False, 200.0, 3000.0)
    ]
    return list_