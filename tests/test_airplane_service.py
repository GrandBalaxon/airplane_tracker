from src.airplane import Airplane
from src.airplane_service import AirplaneService


class FakeStorage:
    def __init__(self, initial_data=None):
        self.data = initial_data or {}
        self.saved_data = None

    def load(self):
        return self.data.copy()

    def save(self, data):
        self.saved_data = data.copy()
        self.data = data.copy()


def test_add_airplane_new(sample_airplanes):
    """Тест добавления нового самолёта."""
    storage = FakeStorage()
    service = AirplaneService(storage)

    plane = sample_airplanes[0]

    service.add_airplane(plane)

    assert plane.airplane_id in storage.data
    assert storage.saved_data is not None


def test_add_airplane_no_duplicates(sample_airplanes):
    """Тест, что одинаковый самолёт не добавляется дважды."""
    plane = sample_airplanes[0]

    initial_data = {
        plane.airplane_id: {
            "country": plane.country,
            "on_ground": plane.on_ground,
            "velocity": plane.velocity,
            "geo_altitude": plane.geo_altitude,
        }
    }

    storage = FakeStorage(initial_data)
    service = AirplaneService(storage)

    service.add_airplane(plane)

    assert len(storage.data) == 1


def test_delete_airplane_existing(sample_airplanes):
    """Тест удаления существующего самолёта."""
    plane = sample_airplanes[0]

    initial_data = {
        plane.airplane_id: {
            "country": plane.country,
            "on_ground": plane.on_ground,
            "velocity": plane.velocity,
            "geo_altitude": plane.geo_altitude,
        }
    }

    storage = FakeStorage(initial_data)
    service = AirplaneService(storage)

    service.delete_airplane(plane.airplane_id)

    assert plane.airplane_id not in storage.data
    assert storage.saved_data is not None


def test_delete_airplane_not_existing():
    """Тест удаления несуществующего самолёта."""
    storage = FakeStorage()
    service = AirplaneService(storage)

    service.delete_airplane("unknown_id")

    assert storage.saved_data is None  # save не должен вызываться


def test_get_airplane_existing(sample_airplanes):
    """Тест получения существующего самолёта."""
    plane = sample_airplanes[0]

    initial_data = {
        plane.airplane_id: {
            "country": plane.country,
            "on_ground": plane.on_ground,
            "velocity": plane.velocity,
            "geo_altitude": plane.geo_altitude,
        }
    }

    storage = FakeStorage(initial_data)
    service = AirplaneService(storage)

    result = service.get_airplane(plane.airplane_id)

    assert result is not None
    assert result.airplane_id == plane.airplane_id
    assert result.country == plane.country


def test_get_airplane_not_existing():
    """Тест получения несуществующего самолёта."""
    storage = FakeStorage()
    service = AirplaneService(storage)

    result = service.get_airplane("unknown")

    assert result is None


def test_get_airplane_invalid_id_type():
    """Тест, что при неверном типе ID возвращается None."""
    storage = FakeStorage()
    service = AirplaneService(storage)

    result = service.get_airplane(123)

    assert result is None


def test_airplane_exists(sample_airplanes):
    """Тест проверки существования самолёта по ID."""
    plane = sample_airplanes[0]

    storage = FakeStorage(
        {
            plane.airplane_id: {
                "country": plane.country,
                "on_ground": plane.on_ground,
                "velocity": plane.velocity,
                "geo_altitude": plane.geo_altitude,
            }
        }
    )

    service = AirplaneService(storage)

    assert service._airplane_exists(plane.airplane_id) is True
    assert service._airplane_exists("unknown") is False


def test_is_same_airplane_data(sample_airplanes):
    """Тест проверки полного совпадения данных самолёта."""
    plane = sample_airplanes[0]

    storage = FakeStorage(
        {
            plane.airplane_id: {
                "country": plane.country,
                "on_ground": plane.on_ground,
                "velocity": plane.velocity,
                "geo_altitude": plane.geo_altitude,
            }
        }
    )

    service = AirplaneService(storage)

    assert service._is_same_airplane_data(plane) is True

    modified_plane = Airplane(
        plane.airplane_id, plane.country, plane.on_ground, plane.velocity + 1, plane.geo_altitude  # изменили
    )

    assert service._is_same_airplane_data(modified_plane) is False


def test_get_airplanes_amount(sample_airplanes):
    """Тест подсчёта количества самолётов."""
    data = {
        plane.airplane_id: {
            "country": plane.country,
            "on_ground": plane.on_ground,
            "velocity": plane.velocity,
            "geo_altitude": plane.geo_altitude,
        }
        for plane in sample_airplanes
    }

    storage = FakeStorage(data)
    service = AirplaneService(storage)

    assert service.get_airplanes_amount() == len(sample_airplanes)
