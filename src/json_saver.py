import json
import logging

from src.airplane import Airplane
from src.base_saver import BaseFileSaver
from src.utils import initialize_json_file
from pathlib import Path

logger = logging.getLogger("json_saver")

class JSONSaver(BaseFileSaver):
    """Класс для сохранения информации о самолётах в JSON-файл.

    Attributes:
        _file_name (str): Имя JSON-файла экземпляра класса.
        _file_path (Path): PATH к рабочему файлу экземпляра класса.
    """

    _file_extension = ".json"

    def __init__(self, file_name: str = "airplanes_data.json"):
        self._file_name = file_name
        self._file_path: Path = self._get_path()

        initialize_json_file(self._file_path)

    def add_airplane(self, airplane: "Airplane") -> None:
        """Метод добавления информации о самолёте в JSON-файл."""
        id_key = airplane.airplane_id
        airplane_data = {
            "country": airplane.country,
            "on_ground": airplane.on_ground,
            "geo_altitude": airplane.geo_altitude,
            "velocity": airplane.velocity
        }

        with open(self._file_path, mode="r") as f:
            data = json.load(f)

        if id_key in data:
            logger.info(f"Обновление информации о борте {id_key}.")
        else:
            logger.info(f"Добавлена информация о борте {id_key}")
        data[id_key] = airplane_data

        with open(self._file_path, mode="w") as f:
            json.dump(data, f, indent=4)

    def get_airplane(self, airplane_id: str) -> "Airplane":
        """Метод получения информации о самолёте из JSON-файла."""
        pass

    def delete_airplane(self, airplane: "Airplane | str") -> None:
        """Метод удаления информации о самолёте из JSON-файла."""
        pass


if __name__ == '__main__':
    uwu = JSONSaver("uwu.json")
    print(uwu._file_path)