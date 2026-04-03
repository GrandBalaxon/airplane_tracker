import json
import logging
from pathlib import Path

from src.airplane import Airplane
from src.base_saver import BaseFileSaver
from src.utils import initialize_file

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

        initialize_file(self._file_path)

    def add_airplane(self, airplane: "Airplane") -> None:
        """Метод добавления информации о самолёте в JSON-файл."""
        try:
            id_key = airplane.airplane_id
            airplane_data = {
                "country": airplane.country,
                "on_ground": airplane.on_ground,
                "geo_altitude": airplane.geo_altitude,
                "velocity": airplane.velocity,
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
        except Exception as e:
            logger.error(f"Возникла ошибка: {e}")
            raise

    def delete_airplane(self, airplane: "Airplane | str") -> None:
        """Метод удаления информации о самолёте из JSON-файла."""
        try:
            if isinstance(airplane, Airplane):
                id_key = airplane.airplane_id
            elif isinstance(airplane, str):
                id_key = airplane
            else:
                raise TypeError(f"Неверный формат {type(airplane)}, ожидается объект класса Airplane или типа str.")

            with open(self._file_path, mode="r") as f:
                data = json.load(f)

            if id_key in data:
                logger.info(f"Удаление информации о борте {id_key}.")
                del data[id_key]
                with open(self._file_path, mode="w") as f:
                    json.dump(data, f, indent=4)
            else:
                logger.info(f"Информация о борте {id_key} не найдена в JSON-файле.")

        except Exception as e:
            logger.error(f"Возникла ошибка: {e}")
            raise

    def get_airplane(self, airplane_id: str) -> "Airplane | None":
        """Метод получения информации о самолёте из JSON-файла."""
        try:
            if not isinstance(airplane_id, str):
                logger.warning(f"Неверный формат ID самолёта: {type(airplane_id)}.")
            else:
                with open(self._file_path, mode="r") as f:
                    data: dict = json.load(f)
                airplane_data = data.get(airplane_id)

                if airplane_data:
                    logger.info(f"Возвращение данных о борте {airplane_id} из JSON-файла.")
                    return Airplane(aircraft_id=airplane_id, **airplane_data)
                else:
                    logger.warning(f"Данных о борте {airplane_id} не найдено в JSON-файле.")

        except Exception as e:
            logger.error(f"Возникла ошибка: {e}")
            raise


if __name__ == "__main__":
    uwu = JSONSaver("uwu.json")
    print(uwu._file_path)
