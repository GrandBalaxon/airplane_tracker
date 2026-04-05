import pytest

from src.airplane import Airplane


@pytest.fixture
def sample_airplanes() -> list[Airplane]:
    return [
        Airplane("p1", "Uzbekistan", False, 100.0, 2000.0),
        Airplane("p2", "USA", False, 200.0, 1000.0),
        Airplane("p3", "Germany", False, 300.0, 2000.0),
        Airplane("p4", "Uzbekistan", True, None, None)
    ]
