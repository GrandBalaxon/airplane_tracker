from unittest.mock import MagicMock

from src.utils import filter_airplanes, generate_filename, get_airplanes_by_altitude, sort_airplanes, get_top_airplanes, \
    print_airplanes, create_saver, save_airplanes


def test_filter_airplanes(sample_airplanes):
    """Тест фильтрации по странам регистрации."""
    result = filter_airplanes(sample_airplanes, "Uzbekistan")
    ids = [plane.airplane_id for plane in result]

    assert ids == ["p1", "p4"]


def test_filter_airplanes_empty_filter(sample_airplanes):
    """Тест, что при пустом фильтре возвращается исходный список."""
    result = filter_airplanes(sample_airplanes, "")

    assert result == sample_airplanes


def test_generate_filename():
    """Тест генерации имени файла (проверяем формат строки)."""
    filename = generate_filename("USA", "JSON")

    assert filename.startswith("USA_")
    assert filename.endswith(".json")


def test_get_airplanes_by_altitude(sample_airplanes):
    """Тест фильтрации по диапазону высот."""
    result = get_airplanes_by_altitude(sample_airplanes, "1500 - 2500")
    ids = [plane.airplane_id for plane in result]

    assert ids == ["p1", "p3"]





def test_get_airplanes_by_altitude_invalid_range(sample_airplanes):
    """Тест обработки некорректного диапазона высот."""
    result = get_airplanes_by_altitude(sample_airplanes, "abc")

    assert result == sample_airplanes


def test_sort_airplanes(sample_airplanes):
    """Тест сортировки самолётов по высоте и скорости (по убыванию)."""
    result = sort_airplanes(sample_airplanes)
    ids = [plane.airplane_id for plane in result]

    assert ids == ["p3", "p1", "p2", "p4"]


def test_get_top_airplanes(sample_airplanes):
    """Тест получения топ N самолётов."""
    result = get_top_airplanes(sample_airplanes, 2)
    ids = [plane.airplane_id for plane in result]

    assert ids == ["p1", "p2"]


def test_get_top_airplanes_invalid(sample_airplanes):
    """Тест обработки некорректного значения N."""
    result = get_top_airplanes(sample_airplanes, 0)

    assert result == sample_airplanes


def test_print_airplanes(sample_airplanes, capsys):
    """Тест вывода списка самолётов в консоль."""
    print_airplanes(sample_airplanes)
    captured = capsys.readouterr()

    assert "Финальный список самолётов" in captured.out
    assert "Борт p1" in captured.out
    assert "Борт p2" in captured.out
    assert "Борт p3" in captured.out
    assert "Борт p4" in captured.out


def test_create_saver_returns_instance():
    """Тест создания saver."""
    mock_saver = MagicMock()
    saver_class = lambda filename: mock_saver

    result = create_saver(saver_class, "file.json")

    assert result is mock_saver


def test_save_airplanes_calls_add(sample_airplanes):
    """Тест сохранения самолётов."""
    mock_saver = MagicMock()
    mock_saver.get_airplanes_amount.return_value = len(sample_airplanes)

    save_airplanes(mock_saver, sample_airplanes)

    assert mock_saver.add_airplane.call_count == len(sample_airplanes)
