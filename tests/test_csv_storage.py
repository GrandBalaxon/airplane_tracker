import csv

from src.csv_storage import CSVStorage


def test_csv_storage_creates_file_if_not_exists(tmp_path):
    """Тест, что CSVStorage создаёт файл с заголовками, если он отсутствует."""
    file_path = tmp_path / "test.csv"

    storage = CSVStorage(str(file_path))

    assert file_path.exists()

    with open(file_path, "r") as f:
        header = f.readline().strip()

    assert "airplane_id" in header


def test_csv_storage_load_empty_file(tmp_path):
    """Тест, что пустой CSV корректно загружается как пустой словарь."""
    file_path = tmp_path / "test.csv"

    with open(file_path, "w") as f:
        f.write("airplane_id,country,on_ground,velocity,geo_altitude\n")

    storage = CSVStorage(str(file_path))
    data = storage.load()

    assert data == {}


def test_csv_storage_save_and_load(sample_airplanes, tmp_path):
    """Тест полного цикла: save -> load."""
    file_path = tmp_path / "test.csv"

    storage = CSVStorage(str(file_path))

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


def test_csv_storage_type_conversion(tmp_path):
    """Тест, что CSV корректно преобразует типы (str -> bool/float)."""
    file_path = tmp_path / "test.csv"

    with open(file_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["airplane_id", "country", "on_ground", "velocity", "geo_altitude"])
        writer.writeheader()
        writer.writerow(
            {
                "airplane_id": "p1",
                "country": "USA",
                "on_ground": "true",
                "velocity": "300.5",
                "geo_altitude": "1500.5",
            }
        )

    storage = CSVStorage(str(file_path))
    data = storage.load()

    plane = data["p1"]

    assert isinstance(plane["velocity"], float)
    assert isinstance(plane["geo_altitude"], float)
    assert isinstance(plane["on_ground"], bool)
    assert plane["on_ground"] is True


def test_csv_storage_overwrites_file(sample_airplanes, tmp_path):
    """Тест, что save перезаписывает файл, а не дописывает."""
    file_path = tmp_path / "test.csv"

    storage = CSVStorage(str(file_path))

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


def test_csv_storage_load_existing_file(tmp_path):
    """Тест, что CSVStorage корректно читает уже существующий файл."""
    file_path = tmp_path / "test.csv"

    with open(file_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["airplane_id", "country", "on_ground", "velocity", "geo_altitude"])
        writer.writeheader()
        writer.writerow(
            {
                "airplane_id": "p1",
                "country": "USA",
                "on_ground": "false",
                "velocity": "200.0",
                "geo_altitude": "1000.0",
            }
        )

    storage = CSVStorage(str(file_path))
    data = storage.load()

    assert "p1" in data
    assert data["p1"]["velocity"] == 200.0
