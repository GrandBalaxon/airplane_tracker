import logging

from src.airplane import Airplane
from src.api import AirplanesAPI
from src.utils import create_saver, filter_aeroplanes, get_aeroplanes_by_altitude, sort_aeroplanes, get_top_aeroplanes, \
    print_aeroplanes

logger = logging.getLogger("main")

def user_interaction() -> None:
    """Функция для взаимодействия с пользователем."""
    country = input("Введите название страны: ")

    api = AirplanesAPI()
    airplanes_raw_data = api.get_airplanes(country)
    if airplanes_raw_data:
        airplanes = Airplane.cast_to_object_list(airplanes_raw_data)

        create_saver(country, airplanes)

        top_n = int(input("Введите количество самолетов для вывода в топ N по высоте полета: "))
        filter_words = input("Введите названия стран для фильтрации по стране регистрации: ").split()
        altitude_range = input("Введите диапазон высот полета: ")

        filtered_aeroplanes = filter_aeroplanes(airplanes, filter_words)
        ranged_aeroplanes = get_aeroplanes_by_altitude(filtered_aeroplanes, altitude_range)
        sorted_aeroplanes = sort_aeroplanes(ranged_aeroplanes)
        top_aeroplanes = get_top_aeroplanes(sorted_aeroplanes, top_n)

        print_aeroplanes(top_aeroplanes)

    else:
        print("Отсутствуют воздушные суда в указанной стране.")


if __name__ == '__main__':
    user_interaction()
