from src.airplane import Airplane


def test_airplanes_lists_sorting(sample_airplanes):
    """Тест правильной работы операторов сравнения при сортировке списка самолётов
    (сначала по высоте, при равенстве — по скорости)."""
    # сортировка по возрастанию
    sorted_list = sorted(sample_airplanes)
    sorted_ids = [plane.airplane_id for plane in sorted_list]

    # сортировка по убыванию
    reversed_list = sorted(sample_airplanes, reverse=True)
    reversed_ids = [plane.airplane_id for plane in reversed_list]

    assert sorted_ids == ["p4", "p2", "p1", "p3"]
    assert reversed_ids == ["p3", "p1", "p2", "p4"]


def test_airplane_on_ground_defaults():
    """Тест, что самолёт на земле получает значения velocity=0 и altitude=0."""
    plane = Airplane("id", "Uzbekistan", True, None, None)
    assert plane.velocity == 0
    assert plane.geo_altitude == 0


def test_airplane_invalid_country_type():
    """Тест обработки некорректного типа страны (не строка)."""
    plane = Airplane("id", 123, False, 100.0, 1000.0)
    assert plane.country == ""


def test_airplanes_equality():
    """Тест проверки равенства двух самолётов по высоте и скорости."""
    a1 = Airplane("id1", "USA", False, 200.0, 1000.0)
    a2 = Airplane("id2", "USA", False, 200.0, 1000.0)
    a3 = Airplane("id3", "USA", False, 300.0, 1000.0)

    assert a1 == a2
    assert a1 != a3
    assert a1 < a3


def test_cast_to_object_list_filters_invalid_data():
    """Тест преобразования списка состояний в объекты Airplane."""
    raw_states = [
        # валидный самолёт
        ["id1", None, "USA", None, None, None, None, None, False, 200.0, None, None, None, 1000.0],
        # валидный самолёт: в воздухе, но без скорости
        ["id2", None, "Germany", None, None, None, None, None, False, None, None, None, None, 1000.0],
        # невалидный: высота вне диапазона
        ["id3", None, "France", None, None, None, None, None, False, 200.0, None, None, None, 50000.0],
        # валидный (на земле, None допустим)
        ["id4", None, "Uzbekistan", None, None, None, None, None, True, None, None, None, None, None],
    ]

    airplanes = Airplane.cast_to_object_list(raw_states)
    ids = [plane.airplane_id for plane in airplanes]

    assert len(airplanes) == 3
    assert ids == ["id1", "id2", "id4"]


def test_airplane_str_and_repr_exact():
    """Тест полного совпадения строковых представлений __str__ и __repr__."""
    plane = Airplane("id1", "USA", False, 200.0, 1000.0)

    assert repr(plane) == (
        "Airplane (icao_id = id1, country = USA, "
        "on_ground = False, velocity = 200.0, geo_altitude = 1000.0)"
    )
    assert str(plane) == "Борт id1 - USA (Скорость: 200.0 м/c, Высота: 1000.0 м)"
