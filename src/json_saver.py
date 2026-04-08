import json
import logging
from pathlib import Path
from typing import Any

from src.airplane import Airplane
from src.base_saver import BaseFileSaver

logger = logging.getLogger("json_saver")


class JSONSaver(BaseFileSaver):
    """Класс для сохранения информации о самолётах в JSON-файл.

    Attributes:
        _file_name (str): Имя JSON-файла экземпляра класса.
        _file_path (Path): PATH к рабочему файлу экземпляра класса.
        _airplanes_data (dict): Датасет с данными о всех текущих самолётах в файле экземпляра класса.
    """

    _file_extension = ".json"

    def __init__(self, file_name: str = "airplanes_data.json"):
        self._file_name = file_name
        self._file_path: Path = self._get_path()
        self._airplanes_data = {}
        self._initialize_file()

    def _get_airplanes_data_from_file(self) -> None:
        """Метод для извлечения данных о самолётах из прикрепленного к объекту класса файла."""
        try:
            if self._file_path.suffix == ".json":
                logger.debug("Идёт работа с JSON-файлом.")
                with open(self._file_path, "r") as file:
                    self._airplanes_data = json.load(file)

            logger.info(f"Из файла выгружены данные о {len(self._airplanes_data)} самолётах.")
            logger.debug(self._airplanes_data)

        except Exception as e:
            logger.error(f"Непредвиденная ошибка: {e}")
            raise

    def _initialize_file(self) -> None:
        """Метод для проверки существования JSON-файла и его инициализации при отсутствии."""
        if not self._file_path.exists():
            logger.info(f"Файл по пути {self._file_path} не найден. Создаем файл с пустым словарём.")
            try:
                if self._file_path.suffix == ".json":
                    with open(self._file_path, "w") as f:
                        json.dump({}, f)

                logger.info(f"Создан файл {self._file_path.name} с пустым словарем.")

            except Exception as e:
                logger.error(f"Ошибка при создании файла: {e}")
                raise
        else:
            logger.info(f"Файл уже существует: {self._file_path}.")
            self._get_airplanes_data_from_file()

    def _write_airplanes_data_to_file(self) -> None:
        """Приватный метод для внесения всех текущих данных из датасета в JSON-файл."""
        with open(self._file_path, mode="w") as file:
            json.dump(self._airplanes_data, file, indent=4)

    def add_airplane(self, airplane: "Airplane") -> None:
        """Метод добавления информации о самолёте в JSON-файл."""
        try:
            if self._is_airplane_in_dataset(airplane):
                logger.info(f"Данные о борте {airplane.airplane_id} уже записаны.")
            else:
                self._add_airplane_to_dataset(airplane)
                self._write_airplanes_data_to_file()

                logger.debug(f"Данные о борте {airplane.airplane_id} записаны в файл.")

        except Exception as e:
            logger.error(f"Возникла ошибка: {e}")
            raise

    def delete_airplane(self, airplane: "Airplane | str") -> None:
        """Метод удаления информации о самолёте из JSON-файла."""
        try:
            id_key = airplane.airplane_id if isinstance(airplane, Airplane) else airplane
            if self._is_airplane_in_dataset(airplane):
                logger.info(f"Данные о борте {id_key} найдены в файле.")

                self._delete_airplane_from_dataset(id_key)
                self._write_airplanes_data_to_file()

                logger.info(f"Данные о борте {id_key} удалены из файла.")

            else:
                logger.info(f"Данные о борте {id_key} не найдены в файле.")

        except Exception as e:
            logger.error(f"Возникла ошибка: {e}")
            raise

    def get_airplane(self, airplane_id: str | Any) -> "Airplane | None":
        """Метод получения информации о самолёте из JSON-файла.

        Args:
            airplane_id (str): Уникальный идентификационный номер самолета по ИКАО, отображаемый в шестнадцатеричном
                формате, как он установлен в транспондере самолета (может быть неверным, пример номера "a50e93")
        """
        try:
            if not isinstance(airplane_id, str):
                logger.warning(f"Неверный формат ID самолёта: {type(airplane_id)}.")
                return None
            else:
                if self._is_airplane_in_dataset(airplane_id):

                    airplane_data = self._airplanes_data.get(airplane_id)
                    if airplane_data is None:
                        return None

                    logger.info(f"Возвращение данных о борте {airplane_id} из JSON-файла.")
                    return Airplane(aircraft_id=airplane_id, **airplane_data)

                else:
                    logger.warning(f"Данных о борте {airplane_id} не найдено в JSON-файле.")
                    return None

        except Exception as e:
            logger.error(f"Возникла ошибка: {e}")
            raise
