import json
import logging
from pathlib import Path

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

                self._delete_airplane_from_dataset(airplane)
                self._write_airplanes_data_to_file()

                logger.info(f"Данные о борте {id_key} удалены из файла.")

            else:
                logger.info(f"Данные о борте {id_key} не найдены в файле.")

        except Exception as e:
            logger.error(f"Возникла ошибка: {e}")
            raise

    def get_airplane(self, airplane_id: str) -> "Airplane | None":
        """Метод получения информации о самолёте из JSON-файла.

        Args:
            airplane_id (str): Уникальный идентификационный номер самолета по ИКАО, отображаемый в шестнадцатеричном
                формате, как он установлен в транспондере самолета (может быть неверным, пример номера "a50e93")
        """
        try:
            if not isinstance(airplane_id, str):
                logger.warning(f"Неверный формат ID самолёта: {type(airplane_id)}.")
            else:
                if self._is_airplane_in_dataset(airplane_id):

                    airplane_data = self._airplanes_data.get(airplane_id)
                    logger.info(f"Возвращение данных о борте {airplane_id} из JSON-файла.")
                    return Airplane(aircraft_id=airplane_id, **airplane_data)

                else:
                    logger.warning(f"Данных о борте {airplane_id} не найдено в JSON-файле.")

        except Exception as e:
            logger.error(f"Возникла ошибка: {e}")
            raise
