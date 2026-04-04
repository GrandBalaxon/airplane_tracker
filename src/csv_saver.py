import csv
import logging
from pathlib import Path

from src.airplane import Airplane
from src.base_saver import BaseFileSaver

logger = logging.getLogger("csv_saver")


class CSVSaver(BaseFileSaver):
    """Класс для сохранения информации о самолётах в CSV-файл.

    Attributes:
        _file_name (str): Имя CSV-файла экземпляра класса.
        _file_path (Path): PATH к рабочему файлу экземпляра класса.
    """

    _file_extension = ".csv"

    def __init__(self, file_name: str = "airplanes_data.csv") -> None:
        self._file_name = file_name
        self._file_path: Path = self._get_path()
        self._airplanes_data = {}
        self._initialize_file()

    def add_airplane(self, airplane: "Airplane") -> None:
        """Абстрактный метод добавления информации о самолёте в файл."""
        try:
            if self._is_airplane_in_dataset(airplane):
                logger.info(f"Данные о борте {airplane.airplane_id} уже записаны.")
            else:
                self._add_airplane_to_dataset(airplane)

                rows = []
                for airplane_id, data in self._airplanes_data.items():
                    rows.append({
                        "airplane_id": airplane_id,
                        "country": data["country"],
                        "on_ground": data["on_ground"],
                        "velocity": data["velocity"],
                        "geo_altitude": data["geo_altitude"]
                    })

                with open(self._file_path, "w", newline="") as file:
                    fieldnames = ["airplane_id", "country", "on_ground", "velocity", "geo_altitude"]
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writeheader()
                    for row in rows:
                        writer.writerow(row)

                logger.info(f"Данные о борте {airplane.airplane_id} записаны в файл.")
                logger.debug(self._airplanes_data)

        except Exception as e:
            logger.error(f"Возникла ошибка: {e}")
            raise

    def delete_airplane(self, airplane: "Airplane") -> None:
        """Абстрактный метод удаления информации о самолёте из файла."""
        pass

    def get_airplane(self, airplane_id: str) -> "Airplane":
        """Абстрактный метод получения информации о самолёте из файла."""
        pass
