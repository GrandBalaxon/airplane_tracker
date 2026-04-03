from pathlib import Path

from src.airplane import Airplane
from src.base_saver import BaseFileSaver
from src.utils import initialize_file


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

        initialize_file(self._file_path)

    def add_airplane(self, airplane: "Airplane") -> None:
        """Абстрактный метод добавления информации о самолёте в файл."""
        pass

    def delete_airplane(self, airplane: "Airplane") -> None:
        """Абстрактный метод удаления информации о самолёте из файла."""
        pass

    def get_airplane(self, airplane_id: str) -> "Airplane":
        """Абстрактный метод получения информации о самолёте из файла."""
        pass
