import logging

from src.airplane import Airplane
from src.api import AirplanesAPI
from src.csv_storage import CSVStorage
from src.json_storage import JSONStorage
from src.utils import (
    create_saver,
    filter_airplanes,
    get_airplanes_by_altitude,
    sort_airplanes,
    get_top_airplanes,
    print_airplanes,
    generate_filename,
    save_airplanes,
)

logger = logging.getLogger("main")


def _get_airplanes_by_country(country: str) -> list[Airplane]:
    """Получение самолётов через API."""
    api = AirplanesAPI()
    raw_data = api.get_airplanes(country)

    if not raw_data:
        return []

    return Airplane.cast_to_object_list(raw_data)


def _choose_saver(country: str, airplanes: list[Airplane]):
    """Выбор формата и создание saver."""
    savers = {
        "JSON": JSONStorage,
        "CSV": CSVStorage
    }

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

        return saver


def _process_airplanes(airplanes: list[Airplane]) -> list[Airplane]:
    """Фильтрация, сортировка и топ."""
    top_n_str = input("Введите количество самолетов для топ N (или Enter): ")
    top_n = int(top_n_str) if top_n_str else 0

    filter_words = input("Введите страны через запятую (или Enter): ")
    altitude_range = input("Введите диапазон высот (или Enter): ")

    result = filter_airplanes(airplanes, filter_words)
    result = get_airplanes_by_altitude(result, altitude_range)
    result = sort_airplanes(result)
    result = get_top_airplanes(result, top_n)

    return result


def user_interaction() -> None:
    """Основная точка входа."""
    country = input("Введите название страны: ")

    airplanes = _get_airplanes_by_country(country)

    if not airplanes:
        print("Отсутствуют воздушные суда в указанной стране.")
        return

    _choose_saver(country, airplanes)

    processed = _process_airplanes(airplanes)

    print_airplanes(processed)


if __name__ == "__main__":
    user_interaction()
