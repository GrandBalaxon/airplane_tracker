from src.airplane import Airplane


def test_airplanes_lists_sorting(sample_airplanes_data):
    """Тестирования правильной работы операторов сравнения при сортировках списков самолётов."""
    list_1 = sample_airplanes_data

    #сортировка по убыванию
    list_2 = sorted(list_1)
    id_list_2 = [x.airplane_id for x in list_2]

    #сортировка по возрастанию
    list_3 = sorted(list_1, reverse=True)
    id_list_3 = [x.airplane_id for x in list_3]

    assert id_list_2 == ["uwu2", "uwu1", "uwu3", "uwu4"]
    assert id_list_3 == ["uwu4", "uwu3", "uwu1", "uwu2"]