import csv

from src.airplane import Airplane
from src.csv_saver import CSVSaver


def test_json_saver_add_and_get(tmp_path):
    """Тест добавления самолёта в CSV и получения его обратно."""
    file_path = tmp_path / "test.csv"
    saver = CSVSaver(str(file_path))

    plane = Airplane("p1", "USA", False, 200.0, 1000.0)

    saver.add_airplane(plane)
    result = saver.get_airplane("p1")

    assert result.airplane_id == "p1"
    assert result.country == "USA"
    assert file_path.exists()


def test_json_saver_no_duplicates(tmp_path):
    """Тест, что один и тот же самолёт не дублируется."""

    file_path = tmp_path / "test.json"
    saver = CSVSaver(str(file_path))

    plane = Airplane("p1", "USA", False, 200.0, 1000.0)

    saver.add_airplane(plane)
    saver.add_airplane(plane)

    assert saver.get_airplanes_amount() == 1


def test_json_saver_delete(tmp_path):
    """Тест удаления самолёта из JSON."""
    file_path = tmp_path / "test.json"
    saver = CSVSaver(str(file_path))

    plane = Airplane("p1", "USA", False, 200.0, 1000.0)

    saver.add_airplane(plane)
    result = saver.get_airplane("p1")
    assert result.airplane_id == "p1"

    saver.delete_airplane("p1")
    result = saver.get_airplane("p1")
    assert result is None
    assert saver.get_airplanes_amount() == 0


def test_csv_saver_loads_existing_file(tmp_path):
    """Тест, что CSVSaver загружает данные из существующего CSV файла."""
    file_path = tmp_path / "test.csv"
    with open(file_path, "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["airplane_id", "country", "on_ground", "velocity", "geo_altitude"]
        )
        writer.writeheader()
        writer.writerow({
            "airplane_id": "p1",
            "country": "USA",
            "on_ground": "False",
            "velocity": "200.0",
            "geo_altitude": "1000.0",
        })

    saver = CSVSaver(str(file_path))
    result = saver.get_airplane("p1")

    assert result.airplane_id == "p1"
    assert result.velocity == 200.0


def test_csv_type_conversion(tmp_path):
    """Тест, что CSV корректно преобразует типы (str -> float/bool)."""
    file_path = tmp_path / "test.csv"
    with open(file_path, "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["airplane_id", "country", "on_ground", "velocity", "geo_altitude"]
        )
        writer.writeheader()
        writer.writerow({
            "airplane_id": "p1",
            "country": "USA",
            "on_ground": "true",
            "velocity": "300.5",
            "geo_altitude": "1500.5",
        })

    saver = CSVSaver(str(file_path))
    plane = saver.get_airplane("p1")

    assert isinstance(plane.velocity, float)
    assert isinstance(plane.geo_altitude, float)
    assert plane.on_ground is True
