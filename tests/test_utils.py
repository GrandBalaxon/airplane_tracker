import re

from src.csv_storage import CSVStorage
from src.utils import (create_saver, filter_airplanes, generate_filename, get_airplanes_by_altitude, get_top_airplanes,
                       save_airplanes, sort_airplanes)


def test_generate_filename_format():
    """Тест, что имя файла генерируется в корректном формате."""
    filename = generate_filename("USA", "JSON")

    assert filename.startswith("USA_")
    assert filename.endswith(".json")

    # Проверяем наличие даты через regex
    pattern = r"USA_\d{2}_\d{2}_\d{4}_\d{2}_\d{2}\.json"
    assert re.match(pattern, filename)


def test_create_saver_instance(tmp_path):
    """Тест создания saver объекта."""
    file_path = tmp_path / "test.csv"

    saver = create_saver(CSVStorage, str(file_path))

    assert isinstance(saver, CSVStorage)
    assert file_path.exists()


def test_save_airplanes(tmp_path, sample_airplanes):
    """Тест сохранения самолётов через сервис."""
    file_path = tmp_path / "test.csv"
    saver = CSVStorage(str(file_path))

    save_airplanes(saver, sample_airplanes)

    # Загружаем данные напрямую
    data = saver.load()

    assert len(data) == len(sample_airplanes)
    assert "p1" in data
    assert data["p1"]["country"] == "Uzbekistan"


def test_filter_airplanes_by_country(sample_airplanes):
    """Тест фильтрации по одной стране."""
    result = filter_airplanes(sample_airplanes, "USA")

    assert len(result) == 1
    assert result[0].country == "USA"


def test_filter_airplanes_multiple_countries(sample_airplanes):
    """Тест фильтрации по нескольким странам."""
    result = filter_airplanes(sample_airplanes, "USA, Germany")

    countries = {plane.country for plane in result}

    assert len(result) == 2
    assert countries == {"USA", "Germany"}


def test_filter_airplanes_empty_filter(sample_airplanes):
    """Тест, что при пустом фильтре возвращается исходный список."""
    result = filter_airplanes(sample_airplanes, "")

    assert result == sample_airplanes


def test_get_airplanes_by_altitude_valid_range(sample_airplanes):
    """Тест фильтрации по корректному диапазону высоты."""
    result = get_airplanes_by_altitude(sample_airplanes, "1000 - 2000")

    for plane in result:
        assert plane.geo_altitude is not None
        assert 1000 <= plane.geo_altitude <= 2000


def test_get_airplanes_by_altitude_invalid_range(sample_airplanes):
    """Тест, что при некорректном диапазоне возвращается исходный список."""
    result = get_airplanes_by_altitude(sample_airplanes, "invalid")

    assert result == sample_airplanes


def test_get_airplanes_by_altitude_empty(sample_airplanes):
    """Тест, что при пустом диапазоне возвращается исходный список."""
    result = get_airplanes_by_altitude(sample_airplanes, "")

    assert result == sample_airplanes


def test_sort_airplanes(sample_airplanes):
    """Тест сортировки самолётов по высоте и скорости."""
    result = sort_airplanes(sample_airplanes)

    # Проверяем порядок убывания
    for i in range(len(result) - 1):
        current = result[i]
        next_plane = result[i + 1]

        assert (current.geo_altitude or 0, current.velocity or 0) >= (
            next_plane.geo_altitude or 0,
            next_plane.velocity or 0,
        )


def test_get_top_airplanes_valid(sample_airplanes):
    """Тест получения топ N самолётов."""
    result = get_top_airplanes(sample_airplanes, 2)

    assert len(result) == 2
    assert result == sample_airplanes[:2]


def test_get_top_airplanes_invalid(sample_airplanes):
    """Тест, что при некорректном top_n возвращается исходный список."""
    result = get_top_airplanes(sample_airplanes, 0)

    assert result == sample_airplanes


def test_get_top_airplanes_non_int(sample_airplanes):
    """Тест, что при неверном типе top_n возвращается исходный список."""
    result = get_top_airplanes(sample_airplanes, "abc")

    assert result == sample_airplanes
