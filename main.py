import logging

from src.airplane import Airplane
from src.api import AirplanesAPI
from src.csv_saver import CSVSaver
from src.json_saver import JSONSaver
from src.utils import create_saver, filter_airplanes, get_airplanes_by_altitude, sort_airplanes, get_top_airplanes, \
    print_airplanes, generate_filename, save_airplanes

logger = logging.getLogger("main")

def user_interaction() -> None:
    """Функция для взаимодействия с пользователем."""
    country = input("Введите название страны: ")

    api = AirplanesAPI()
    airplanes_raw_data = api.get_airplanes(country)
    if airplanes_raw_data:
        airplanes = Airplane.cast_to_object_list(airplanes_raw_data)

        savers = {"JSON": JSONSaver, "CSV": CSVSaver}

        while True:
            file_extension = input("Выберите формат файла (JSON/CSV): ").upper()
            saver_class = savers.get(file_extension)

            if not saver_class:
                print("Неверный формат.")
                continue

            file_name = input("Введите имя файла (или Enter): ").strip()
            if not file_name:
                file_name = generate_filename(country, file_extension)

            saver = create_saver(saver_class, file_name)
            save_airplanes(saver, airplanes)
            break

        top_n_str = input("Введите количество самолетов для вывода в топ N по высоте полета (или Enter): ")
        top_n = int(top_n_str) if top_n_str != "" else 0
        filter_words = input("Введите названия стран для фильтрации через запятую (или Enter): ")
        altitude_range = input("Введите диапазон высот полета (или Enter): ")

        filtered_aeroplanes = filter_airplanes(airplanes, filter_words)
        ranged_aeroplanes = get_airplanes_by_altitude(filtered_aeroplanes, altitude_range)
        sorted_aeroplanes = sort_airplanes(ranged_aeroplanes)
        top_aeroplanes = get_top_airplanes(sorted_aeroplanes, top_n)

        print_airplanes(top_aeroplanes)

    else:
        print("Отсутствуют воздушные суда в указанной стране.")


if __name__ == '__main__':
    user_interaction()
