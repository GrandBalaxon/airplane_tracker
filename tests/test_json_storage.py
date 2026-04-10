import json

from src.json_storage import JSONStorage


def test_json_storage_creates_file_if_not_exists(tmp_path):
    """Тест, что JSONStorage создаёт файл с пустым словарём, если он отсутствует."""
    file_path = tmp_path / "test.json"

    storage = JSONStorage(str(file_path))

    assert file_path.exists()

    with open(file_path, "r") as f:
        data = json.load(f)

    assert data == {}


def test_json_storage_load_empty_file(tmp_path):
    """Тест, что пустой JSON корректно загружается."""
    file_path = tmp_path / "test.json"

    with open(file_path, "w") as f:
        json.dump({}, f)

    storage = JSONStorage(str(file_path))
    data = storage.load()

    assert data == {}


def test_json_storage_save_and_load(sample_airplanes, tmp_path):
    """Тест полного цикла: save -> load."""
    file_path = tmp_path / "test.json"

    storage = JSONStorage(str(file_path))

    data = {
        plane.airplane_id: {
            "country": plane.country,
            "on_ground": plane.on_ground,
            "velocity": plane.velocity,
            "geo_altitude": plane.geo_altitude,
        }
        for plane in sample_airplanes
    }

    storage.save(data)
    loaded = storage.load()

    assert len(loaded) == len(sample_airplanes)

    for plane in sample_airplanes:
        assert plane.airplane_id in loaded


def test_json_storage_overwrites_file(tmp_path):
    """Тест, что save перезаписывает файл."""
    file_path = tmp_path / "test.json"

    storage = JSONStorage(str(file_path))

    data1 = {
        "p1": {
            "country": "USA",
            "on_ground": False,
            "velocity": 100.0,
            "geo_altitude": 1000.0,
        }
    }

    data2 = {
        "p2": {
            "country": "Germany",
            "on_ground": True,
            "velocity": 200.0,
            "geo_altitude": 2000.0,
        }
    }

    storage.save(data1)
    storage.save(data2)

    loaded = storage.load()

    assert "p1" not in loaded
    assert "p2" in loaded
    assert len(loaded) == 1


def test_json_storage_load_existing_file(tmp_path):
    """Тест, что JSONStorage корректно читает уже существующий файл."""
    file_path = tmp_path / "test.json"

    data = {
        "p1": {
            "country": "USA",
            "on_ground": False,
            "velocity": 200.0,
            "geo_altitude": 1000.0,
        }
    }

    with open(file_path, "w") as f:
        json.dump(data, f)

    storage = JSONStorage(str(file_path))
    loaded = storage.load()

    assert "p1" in loaded
    assert loaded["p1"]["velocity"] == 200.0


def test_json_storage_invalid_json_returns_empty_dict(tmp_path):
    """Тест обработки JSONDecodeError."""
    file_path = tmp_path / "test.json"

    with open(file_path, "w") as f:
        f.write("{ invalid json")

    storage = JSONStorage(str(file_path))
    data = storage.load()

    assert data == {}


def test_json_storage_invalid_format_returns_empty_dict(tmp_path):
    """Тест, что если JSON не dict — возвращается пустой словарь."""
    file_path = tmp_path / "test.json"

    with open(file_path, "w") as f:
        json.dump(["not", "a", "dict"], f)

    storage = JSONStorage(str(file_path))
    data = storage.load()

    assert data == {}