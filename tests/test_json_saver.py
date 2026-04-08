import json

from src.airplane import Airplane
from src.json_saver import JSONSaver


def test_json_saver_add_and_get(tmp_path):
    """Тест добавления самолёта в JSON и получения его обратно."""
    file_path = tmp_path / "test.json"
    saver = JSONSaver(str(file_path))

    plane = Airplane("p1", "USA", False, 200.0, 1000.0)

    saver.add_airplane(plane)
    result = saver.get_airplane("p1")

    assert result.airplane_id == "p1"
    assert result.country == "USA"
    assert file_path.exists()


def test_json_saver_no_duplicates(tmp_path):
    """Тест, что один и тот же самолёт не дублируется."""

    file_path = tmp_path / "test.json"
    saver = JSONSaver(str(file_path))

    plane = Airplane("p1", "USA", False, 200.0, 1000.0)

    saver.add_airplane(plane)
    saver.add_airplane(plane)

    assert saver.get_airplanes_amount() == 1


def test_json_saver_delete(tmp_path):
    """Тест удаления самолёта из JSON."""
    file_path = tmp_path / "test.json"
    saver = JSONSaver(str(file_path))

    plane = Airplane("p1", "USA", False, 200.0, 1000.0)

    saver.add_airplane(plane)
    result = saver.get_airplane("p1")
    assert result.airplane_id == "p1"

    saver.delete_airplane("p1")
    result = saver.get_airplane("p1")
    assert result is None
    assert saver.get_airplanes_amount() == 0


def test_json_saver_loads_existing_file(tmp_path):
    """Тест, что JSONSaver загружает данные из существующего файла."""
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

    saver = JSONSaver(str(file_path))
    result = saver.get_airplane("p1")

    assert result.airplane_id == "p1"
    assert result.country == "USA"


def test_json_empty_file(tmp_path):
    """Тест, что пустой JSON файл не ломает загрузку."""
    file_path = tmp_path / "test.json"
    with open(file_path, "w") as f:
        f.write("{}")

    saver = JSONSaver(str(file_path))

    assert saver.get_airplane("p1") is None


def test_get_airplanes_data_json_decode_error(tmp_path):
    """Тест обработка случая JSONDecodeError."""
    file_path = tmp_path / "test.json"
    with open(file_path, "w") as f:
        f.write("{ invalid json")

    saver = JSONSaver(str(file_path.name))
    saver._file_path = file_path

    saver._get_airplanes_data_from_file()
    assert saver._airplanes_data == {}


def test_get_airplane_invalid_id_type(tmp_path):
    """Тест, что JSONSaver возвращает None при передаче некорректного типа airplane_id."""
    file_path = tmp_path / "test.json"
    with open(file_path, "w") as f:
        f.write("{}")

    saver = JSONSaver(str(file_path.name))
    saver._file_path = file_path

    result = saver.get_airplane(123)
    assert result is None


def test_is_airplane_in_empty_dataset(tmp_path):
    """Тест, что при пустом датасете самолёт не находится."""
    saver = JSONSaver("test.json")
    saver._airplanes_data = {}

    result = saver._is_airplane_in_dataset("abc123")

    assert result is False
