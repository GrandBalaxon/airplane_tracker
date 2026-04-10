import csv
import logging
from pathlib import Path
from typing import Any

from src.file_storage import FileStorage

logger = logging.getLogger("csv_storage")


class CSVStorage(FileStorage):
    """Класс для сохранения информации о самолётах в CSV-файл.

    Attributes:
        _file_name (str): Имя CSV-файла-хранилища экземпляра класса.
        _file_path (Path): PATH к рабочему CSV-файлу-хранилищу экземпляра класса.
    """

    _file_extension = ".csv"

    def __init__(self, file_name: str | None = None):
        super().__init__(file_name)

    def _default_file_name(self) -> str:
        return "airplanes_data.csv"

    def load(self) -> dict[str, Any]:
        """Метод для загрузки данных о самолётах из прикрепленного к объекту класса CSV-файла."""
        try:
            with open(self._file_path, "r") as file:
                dict_reader = csv.DictReader(file)
                result = {}
                for data in dict_reader:
                    result[data["airplane_id"]] = {
                        "country": data["country"],
                        "on_ground": True if data["on_ground"].lower() == "true" else False,
                        "velocity": float(data["velocity"]),
                        "geo_altitude": float(data["geo_altitude"]),
                    }

                logger.debug(f"Из файла выгружены данные.")
                return result

        except Exception as e:
            logger.error(f"Непредвиденная ошибка: {e}")
            raise

    def _initialize_file(self) -> None:
        """Метод для проверки существования CSV-файла и его инициализации при отсутствии."""
        if not self._file_path.exists():
            logger.info(f"Файл по пути {self._file_path} не найден. Создаем CSV-файл с заголовками.")
            try:
                with open(self._file_path, "w", newline="") as file:
                    fieldnames = ["airplane_id", "country", "on_ground", "velocity", "geo_altitude"]
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writeheader()

                logger.info(f"Создан CSV-файл {self._file_path.name} с заголовками.")

            except Exception as e:
                logger.error(f"Ошибка при создании файла: {e}")
                raise
        else:
            logger.info(f"Файл уже существует: {self._file_path}.")

    def save(self, data: dict[str, Any]) -> None:
        """Приватный метод для внесения всех текущих данных из датасета в CSV-файл."""
        rows = []
        for airplane_id, airplane_data in data.items():
            rows.append(
                {
                    "airplane_id": airplane_id,
                    "country": airplane_data["country"],
                    "on_ground": airplane_data["on_ground"],
                    "velocity": airplane_data["velocity"],
                    "geo_altitude": airplane_data["geo_altitude"],
                }
            )

        with open(self._file_path, "w", newline="") as file:
            fieldnames = ["airplane_id", "country", "on_ground", "velocity", "geo_altitude"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                writer.writerow(row)
