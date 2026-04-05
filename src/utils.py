import logging
from datetime import datetime

from src.airplane import Airplane
from src.csv_saver import CSVSaver
from src.json_saver import JSONSaver

logger = logging.getLogger("utils")


def generate_filename(country: str, extension: str) -> str:
    now = datetime.now()
    return (
        f"{country}_"
        f"{now.day:02d}_{now.month:02d}_{now.year}_"
        f"{now.hour:02d}_{now.minute:02d}."
        f"{extension.lower()}"
    )


def create_saver(country: str, airplanes: list[Airplane]) -> None:
    """Функция для выбора расширения файла для сохранения базы данных с самолётами и создания saver объекта."""
    while True:
        file_extension = input("Выберите формат файла для сохранения (JSON/CSV): ").upper()
        if file_extension == "JSON":
            file_name = input("Введите имя файла (или Enter): ")
            if file_name == "":
                saver = JSONSaver(generate_filename(country, file_extension))
            else:
                saver = JSONSaver(file_name)
            for data in airplanes:
                saver.add_airplane(data)
            logger.info(f"добавлено {JSONSaver.get_airplanes_amount} в JSON-файл.")
            break
        elif file_extension == "CSV":
            file_name = input("Введите имя файла (или Enter): ")
            if file_name == "":
                saver = CSVSaver(generate_filename(country, file_extension))
            else:
                saver = CSVSaver(file_name)
            for data in airplanes:
                saver.add_airplane(data)
            logger.info(f"добавлено {saver.get_airplanes_amount} в CSV-файл.")
            break
        else:
            print("Указан не верный формат.")


def filter_aeroplanes(airplanes: list[Airplane], filter_words: list[str]) -> list[Airplane]:
    """Функция для фильтрации списка объектов класса Airplane по стране регистрации.

    Args:
        airplanes (list[Airplane]): Список объектов класса Airplanes
        filter_words (list[str]): Список стран для фильтрации
    """
    try:
        if filter_words:
            logger.info(f"Список фильтрации: {filter_words}.")
            filtered_list = [plane for plane in airplanes if plane.country in filter_words]
            return filtered_list
        else:
            logger.info("Не указано стран для фильтрации списка.")
            return airplanes

    except Exception as e:
        logger.error(f"Возникла ошибка: {e}")
        raise
