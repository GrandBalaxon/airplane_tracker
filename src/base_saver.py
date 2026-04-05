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

    def _add_airplane_to_dataset(self, airplane: "Airplane") -> None:
        """Метод для добавления данных в датасет экземпляра класса."""
        id_key = airplane.airplane_id
        airplane_data = {
            "country": airplane.country,
            "on_ground": airplane.on_ground,
            "geo_altitude": airplane.geo_altitude,
            "velocity": airplane.velocity,
        }
        self._airplanes_data[id_key] = airplane_data

    def _delete_airplane_from_dataset(self, airplane: "Airplane") -> None:
        """Метод удаления данных о самолёте из датасета."""
        id_key = airplane.airplane_id
        del self._airplanes_data[id_key]

    def _get_airplanes_data_from_file(self) -> None:
        """Метод для извлечения данных о самолётах из прикрепленного к объекту класса файла."""
        try:
            # Если идёт работа с JSON-файлом
            if self._file_path.suffix == ".json":
                logger.debug("Идёт работа с JSON-файлом.")
                with open(self._file_path, "r") as file:
                    self._airplanes_data = json.load(file)

            # Если идёт работа с CSV-файлом
            if self._file_path.suffix == ".csv":
                logger.debug("Идёт работа с CSV-файлом.")

                with open(self._file_path, "r") as file:
                    dict_reader = csv.DictReader(file)
                    for data in dict_reader:

                        airplane_id = data["airplane_id"]
                        country = data["country"]
                        on_ground = True if "true" in data["on_ground"].lower() else False
                        geo_altitude = float(data["geo_altitude"])
                        velocity = float(data["velocity"])

                        airplane = Airplane(airplane_id, country, on_ground, velocity, geo_altitude)
                        self._add_airplane_to_dataset(airplane)

                        logger.debug(f"Добавлена информация о {airplane.airplane_id} в датасет.")

            logger.info(f"Из файла выгружены данные о {len(self._airplanes_data)} самолётах.")
            logger.debug(self._airplanes_data)

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
                    with open(self._file_path, "w", newline="") as file:
                        fieldnames = ["airplane_id", "country", "on_ground", "velocity", "geo_altitude"]
                        writer = csv.DictWriter(file, fieldnames=fieldnames)
                        writer.writeheader()

                logger.info(f"Создан файл {self._file_path.name} с пустым словарем.")

            except Exception as e:
                logger.error(f"Ошибка при создании файла: {e}")
                raise
        else:
            logger.info(f"Файл уже существует: {self._file_path}.")
            self._get_airplanes_data_from_file()

    def _get_path(self) -> Path:
        """Метод для получения PATH к рабочему файлу."""
        if self._file_name.endswith(self.__class__._file_extension):
            return Path(__file__).parent.parent / "data" / self._file_name
        else:
            return Path(__file__).parent.parent / "data" / f"{self._file_name}{self.__class__._file_extension}"

    def _is_airplane_in_dataset(self, airplane: "Airplane | str") -> bool | None:
        """
        Метод проверки наличия данных о самолёте в датасете экземпляра класса.

        Если на вход даётся объект класса "Airplane" - то проверяет все его данные.
        При точном совпадении всех данных о борте - возвращает True.

        Если на вход даётся строка с "airplane_id", то проверяется наличие данных о данном самолёте по его ID.
        """
        try:
            if len(self._airplanes_data) == 0:
                file_extension = self.__class__._file_extension[1:].upper()
                logger.info(f"Датасет/{file_extension}-файл пока что пуст.")
                return False
            else:
                if isinstance(airplane, Airplane):
                    id_key = airplane.airplane_id

                    if id_key in self._airplanes_data:
                        if (
                            self._airplanes_data[id_key]["country"] == airplane.country
                            and self._airplanes_data[id_key]["on_ground"] == airplane.on_ground
                            and self._airplanes_data[id_key]["velocity"] == airplane.velocity
                            and self._airplanes_data[id_key]["geo_altitude"] == airplane.geo_altitude
                        ):
                            return True
                        else:
                            return False
                    else:
                        return False

                elif isinstance(airplane, str):
                    if airplane in self._airplanes_data:
                        return True
                    else:
                        return False

                else:
                    raise TypeError(f"Неверный формат {type(airplane)}, ожидается объект класса Airplane или str.")

        except Exception as e:
            logger.error(f"Непредвиденная ошибка: {e}")
            raise

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

    def get_airplanes_amount(self) -> int:
        """Геттер выдающий текущее количество самолетов в датасете/файле экземпляра класса."""
        if len(self._airplanes_data) > 0:
            return len(self._airplanes_data)
        else:
            return 0
