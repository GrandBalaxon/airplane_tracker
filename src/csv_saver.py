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
        _airplanes_data (dict): датасет с данными о всех текущих самолётах в файле экземпляра класса.
    """

    _file_extension = ".csv"

    def __init__(self, file_name: str = "airplanes_data.csv") -> None:
        self._file_name = file_name
        self._file_path: Path = self._get_path()
        self._airplanes_data = {}
        self._initialize_file()

    def _write_airplanes_data_to_file(self) -> None:
        """Приватный метод для внесения всех текущих данных из датасета в файл."""
        rows = []
        for airplane_id, data in self._airplanes_data.items():
            rows.append(
                {
                    "airplane_id": airplane_id,
                    "country": data["country"],
                    "on_ground": data["on_ground"],
                    "velocity": data["velocity"],
                    "geo_altitude": data["geo_altitude"],
                }
            )

        with open(self._file_path, "w", newline="") as file:
            fieldnames = ["airplane_id", "country", "on_ground", "velocity", "geo_altitude"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                writer.writerow(row)

    def add_airplane(self, airplane: "Airplane") -> None:
        """Абстрактный метод добавления информации о самолёте в файл."""
        try:
            if self._is_airplane_in_dataset(airplane):
                logger.info(f"Данные о борте {airplane.airplane_id} уже записаны.")
            else:
                self._add_airplane_to_dataset(airplane)
                self._write_airplanes_data_to_file()

                logger.info(f"Данные о борте {airplane.airplane_id} записаны в файл.")

        except Exception as e:
            logger.error(f"Возникла ошибка: {e}")
            raise

    def delete_airplane(self, airplane: "Airplane") -> None:
        """Абстрактный метод удаления информации о самолёте из файла."""
        try:
            if self._is_airplane_in_dataset(airplane):
                logger.info(f"Данные о борте {airplane.airplane_id} найдены в файле.")

                self._delete_airplane_from_dataset(airplane)
                self._write_airplanes_data_to_file()

                logger.info(f"Данные о борте {airplane.airplane_id} удалены из файла.")

            else:
                logger.info(f"Данные о борте {airplane.airplane_id} не найдены в файле.")

        except Exception as e:
            logger.error(f"Возникла ошибка: {e}")
            raise

    def get_airplane(self, airplane_id: str) -> "Airplane":
        """Абстрактный метод получения информации о самолёте из файла."""
        pass
