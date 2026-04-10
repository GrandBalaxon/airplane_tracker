import json
import logging
from json import JSONDecodeError
from pathlib import Path
from typing import Any

from src.airplane import Airplane
from src.base_storage import BaseStorage

logger = logging.getLogger("json_storage")


class JSONStorage(BaseStorage):
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
        """Метод для извлечения данных о самолётах из прикрепленного к объекту класса JSON-файла."""
        try:
            with open(self._file_path, "r") as file:
                self._airplanes_data = json.load(file)

            logger.info(f"Из файла выгружены данные о {self.get_airplanes_amount()} самолётах.")

        except JSONDecodeError as e:
            logger.warning(f"Ошибка декодирования JSON ({self._file_path.name}): {e}. Используется пустой датасет.")
            self._airplanes_data = {}
        except Exception as e:
            logger.error(f"Непредвиденная ошибка: {e}")
            raise

    def _initialize_file(self) -> None:
        """Метод для проверки существования JSON-файла и его инициализации при отсутствии."""
        if not self._file_path.exists():
            logger.info(f"Файл по пути {self._file_path} не найден. Создаем файл с пустым словарём.")
            try:
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
