import logging
import re
from datetime import datetime

from src.airplane import Airplane
from src.base_saver import BaseStorage

logger = logging.getLogger("utils")


def generate_filename(country: str, extension: str) -> str:
    now = datetime.now()
    return (
        f"{country}_"
        f"{now.day:02d}_{now.month:02d}_{now.year}_"
        f"{now.hour:02d}_{now.minute:02d}."
        f"{extension.lower()}"
    )


def create_saver(saver_class: type, file_name: str) -> BaseStorage:
    """Создаёт и возвращает экземпляр saver."""
    return saver_class(file_name)


def save_airplanes(saver: BaseStorage, airplanes: list[Airplane]) -> None:
    """Сохраняет список самолётов в saver."""
    for airplane in airplanes:
        saver.add_airplane(airplane)

    logger.info(f"Добавлено {saver.get_airplanes_amount()} самолётов в файл.")


def filter_airplanes(airplanes: list[Airplane], filter_words: str) -> list[Airplane]:
    """Функция для фильтрации списка объектов класса Airplane по стране регистрации.

    Args:
        airplanes (list[Airplane]): Список объектов класса Airplanes
        filter_words (list[str]): Список стран для фильтрации
    """
    try:
        if filter_words:
            logger.info(f"Список фильтрации: {filter_words}.")
            country_list = [x.strip().lower() for x in filter_words.split(",")]

            filtered_list = [plane for plane in airplanes if plane.country.lower().strip() in country_list]

            logger.info(f"Отфильтровано по странам {len(filtered_list)} самолётов.")
            for country in country_list:
                logger.info(
                    f"{country.title()}: {len([x for x in filtered_list if x.country.lower().strip() == country])}."
                )

            return filtered_list
        else:
            logger.info("Не указано стран для фильтрации списка.")
            return airplanes

    except Exception as e:
        logger.error(f"Возникла ошибка: {e}")
        raise


def get_airplanes_by_altitude(airplanes: list[Airplane], altitude_range: str) -> list[Airplane]:
    """Функция для фильтрации списка объектов класса Airplane по геометрической высоте.

    Args:
        airplanes (list[Airplane]): Список объектов класса Airplanes
        altitude_range (str): Перепад геометрических высок для фильтрации (Пример: 100000 - 150000)
    """
    try:
        if altitude_range:
            alt_range_cleaned = list(map(int, re.findall(r"\d+", altitude_range)))
            if len(alt_range_cleaned) == 2:
                logger.info(f"Высоты для фильтрации: {alt_range_cleaned[0]} - {alt_range_cleaned[1]}.")
                filtered_list = [
                    plane for plane in airplanes if alt_range_cleaned[0] <= plane.geo_altitude <= alt_range_cleaned[1]
                ]
                return filtered_list
            else:
                logger.warning(f"Неверно указан диапазон высот: {altitude_range}.")
                return airplanes
        else:
            logger.info(f"Не был указан диапазон высот.")
            return airplanes

    except Exception as e:
        logger.error(f"Возникла ошибка: {e}")
        raise


def sort_airplanes(airplanes: list[Airplane]) -> list[Airplane]:
    """Функция для сортировки самолётов по высоте."""
    try:
        sorted_aeroplanes = sorted(airplanes, key=lambda x: (x.geo_altitude, x.velocity), reverse=True)
        return sorted_aeroplanes

    except Exception as e:
        logger.error(f"Возникла ошибка: {e}")
        return airplanes


def get_top_airplanes(airplanes: list[Airplane], top_n: int) -> list[Airplane]:
    """Функция выдаёт N самолётов из списка.

    Args:
        airplanes (list[Airplane]): Список объектов класса Airplanes
        top_n (int): Число N - количество выдаваемых функцией позиций самолётов
    """
    try:
        if isinstance(top_n, int) and top_n != 0:
            top_list = airplanes[:top_n]
            logger.info(f"Отсеяно топ {top_n} самолётов.")
            return top_list
        else:
            logger.warning("Не указано число N.")
            return airplanes

    except Exception as e:
        logger.error(f"Возникла ошибка: {e}")
        return airplanes


def print_airplanes(airplanes: list[Airplane]) -> None:
    """Функция для вывода списка самолётов на экран."""
    try:
        print("\nФинальный список самолётов:")
        for airplane in airplanes:
            print(airplane)

    except Exception as e:
        logger.error(f"Возникла ошибка: {e}")
        raise
