import csv
import json
import logging
from abc import ABC, abstractmethod
from pathlib import Path

from src.airplane import Airplane

logger = logging.getLogger("base_saver")

class BaseFileSaver(ABC):
    """Абстрактный базовый класс для сохранения в различные типы файлов."""

    _file_extension = ""

    __slots__ = ["_file_name", "_file_path", "_airplanes_data"]

    def _get_airplanes_data_from_file(self) -> dict | None:
        """Метод для извлечения данных о самолётах из прикрепленного к объекту класса файла."""
        try:
            # Если идёт работа с JSON-файлом
            if self._file_path.suffix == ".json":
                with open(self._file_path, "r") as file:
                    airplanes_data: dict = json.load(file)
                    return airplanes_data

            # Если идёт работа с CSV-файлом
            if self._file_path.suffix == ".csv":
                airplanes_data = {}
                with open(self._file_path, 'r') as file:
                    dict_reader = csv.DictReader(file)
                    for data in dict_reader:
                        airplanes_data[data["airplane_id"]] = {
                            "country": data.country,
                            "on_ground": data.on_ground,
                            "geo_altitude": data.geo_altitude,
                            "velocity": data.velocity,
                        }
                    return airplanes_data

        except Exception as e:
            logger.error(f"Непредвиденная ошибка: {e}")
            raise

    def _initialize_file(self) -> None:
        """Метод для проверки существования файла и его инициализации при отсутствии."""
        if not self._file_path.exists():
            logger.info(f"Файл по пути {self._file_path} не найден. Создаем json файл с пустым словарём.")
            try:
                # Если идёт работа с JSON-файлом
                if self._file_path.suffix == ".json":
                    with open(self._file_path, "w") as f:
                        json.dump({}, f)

                # Если идёт работа с CSV-файлом
                if self._file_path.suffix == ".csv":
                    with open(self._file_path, 'w', newline='') as file:
                        fieldnames = ["airplane_id", "country", "on_ground", "velocity", "geo_altitude"]
                        writer = csv.DictWriter(file, fieldnames=fieldnames)
                        writer.writeheader()

                logger.info(f"Создан файл {self._file_path.name} с пустым словарем.")

            except Exception as e:
                logger.error(f"Ошибка при создании файла: {e}")
                raise
        else:
            logger.info(f"Файл уже существует: {self._file_path}.")
            self._airplanes_data: dict = self._get_airplanes_data_from_file()
            logger.info(f"Из файла выгружены данные о {len(self._airplanes_data)} самолётах.")

    def _get_path(self) -> Path:
        """Метод для получения PATH к рабочему файлу."""
        if self._file_name.endswith(self.__class__._file_extension):
            return Path(__file__).parent.parent / "data" / self._file_name
        else:
            return Path(__file__).parent.parent / "data" / f"{self._file_name}{self.__class__._file_extension}"

    @abstractmethod
    def add_airplane(self, airplane: "Airplane") -> None:
        """Абстрактный метод добавления информации о самолёте в файл."""
        pass

    @abstractmethod
    def delete_airplane(self, airplane: "Airplane") -> None:
        """Абстрактный метод удаления информации о самолёте из файла."""
        pass

    @abstractmethod
    def get_airplane(self, airplane_id: str) -> "Airplane":
        """Абстрактный метод получения информации о самолёте из файла."""
        pass
