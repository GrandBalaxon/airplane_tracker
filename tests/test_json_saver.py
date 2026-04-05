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
