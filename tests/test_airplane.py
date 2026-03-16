from src.airplane import Airplane


def test_airplanes_lists_sorting(sample_airplanes_data):
    """Тестирования правильной работы операторов сравнения при сортировках списков самолётов."""
    list_1 = sample_airplanes_data
    id_list_1 = [x.aircraft_id for x in list_1]

    #сортировка по убыванию
    list_2 = sorted(list_1)
    id_list_2 = [x.aircraft_id for x in list_2]

    assert id_list_2 == ["uwu2", "uwu1", "uwu3", "uwu4"]