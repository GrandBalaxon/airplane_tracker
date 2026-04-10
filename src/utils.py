import logging
import re
from datetime import datetime
from typing import Type

from src.airplane import Airplane
from src.airplane_service import AirplaneService
from src.file_storage import FileStorage

logger = logging.getLogger("utils")


def generate_filename(country: str, extension: str) -> str:
    """Генерация имени файла."""
    now = datetime.now()
    return (
        f"{country}_"
        f"{now.day:02d}_{now.month:02d}_{now.year}_"
        f"{now.hour:02d}_{now.minute:02d}."
        f"{extension.lower()}"
    )


def create_saver(saver_class: Type[FileStorage], file_name: str) -> FileStorage:
    """Создаёт экземпляр saver."""
    return saver_class(file_name)


def save_airplanes(saver: FileStorage, airplanes: list[Airplane]) -> None:
    """Сохраняет список самолётов через сервис."""
    service = AirplaneService(saver)

    for airplane in airplanes:
        service.add_airplane(airplane)

    logger.info(f"Сохранено {service.get_airplanes_amount()} самолётов.")


def _parse_countries(filter_words: str) -> list[str]:
    """Парсит строку стран в список."""
    return [word.strip().lower() for word in filter_words.split(",") if word.strip()]


def filter_airplanes(airplanes: list[Airplane], filter_words: str) -> list[Airplane]:
    """Фильтрация по странам."""
    if not filter_words:
        logger.info("Фильтр стран не задан.")
        return airplanes

    countries = _parse_countries(filter_words)
    logger.info(f"Фильтрация по странам: {countries}")

    return [plane for plane in airplanes if plane.country and plane.country.lower().strip() in countries]


def _parse_altitude_range(altitude_range: str) -> tuple[int, int] | None:
    """Парсит диапазон высот."""
    numbers = list(map(int, re.findall(r"\d+", altitude_range)))
    return (numbers[0], numbers[1]) if len(numbers) == 2 else None


def get_airplanes_by_altitude(airplanes: list[Airplane], altitude_range: str) -> list[Airplane]:
    """Фильтрация по высоте."""
    if not altitude_range:
        logger.info("Диапазон высот не задан.")
        return airplanes

    parsed = _parse_altitude_range(altitude_range)
    if not parsed:
        logger.warning(f"Некорректный диапазон высот: {altitude_range}")
        return airplanes

    min_alt, max_alt = parsed
    logger.info(f"Фильтрация по высоте: {min_alt} - {max_alt}")

    return [
        plane for plane in airplanes if plane.geo_altitude is not None and min_alt <= plane.geo_altitude <= max_alt
    ]


def sort_airplanes(airplanes: list[Airplane]) -> list[Airplane]:
    """Сортировка по высоте и скорости."""
    return sorted(airplanes, key=lambda x: (x.geo_altitude or 0, x.velocity or 0), reverse=True)


def get_top_airplanes(airplanes: list[Airplane], top_n: int) -> list[Airplane]:
    """Возвращает топ N самолётов."""
    if not isinstance(top_n, int) or top_n <= 0:
        logger.info("Топ N не задан.")
        return airplanes

    logger.info(f"Возвращаем топ {top_n} самолётов.")
    return airplanes[:top_n]


def print_airplanes(airplanes: list[Airplane]) -> None:
    """Вывод самолётов."""
    print("\nФинальный список самолётов:")
    for airplane in airplanes:
        print(airplane)
