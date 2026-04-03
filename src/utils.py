import json
import csv
import logging
from pathlib import Path

logger = logging.getLogger("utils")


def initialize_file(file_path: Path) -> None:
    """Функция для проверки существования файла и его инициализации при отсутствии."""
    if not file_path.exists():
        logger.info(f"Файл по пути {file_path} не найден. Создаем json файл с пустым словарём.")
        try:
            # Если идёт работа с JSON-файлом
            if file_path.suffix == ".json":
                with open(file_path, "w") as f:
                    json.dump({}, f)

            # Если идёт работа с CSV-файлом
            if file_path.suffix == ".csv":
                with open(file_path, 'w', newline='') as file:
                    fieldnames = ["airplane_id", "country", "on_ground", "velocity", "geo_altitude"]
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writeheader()

            logger.info(f"Создан файл {file_path.name} с пустым словарем.")

        except Exception as e:
            logger.error(f"Ошибка при создании файла: {e}")
            raise
    else:
        logger.info(f"Файл уже существует: {file_path}.")
