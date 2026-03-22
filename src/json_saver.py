import json
from pathlib import Path

from src.airplane import Airplane
from src.base_saver import BaseFileSaver


class JSONSaver(BaseFileSaver):
    """Класс для сохранения информации о самолётах в JSON-файл.

    Attributes:
        _file_name (str): Имя JSON-файла экземпляра класса.
        _file_path (str): PATH к рабочему файлу экземпляра класса.
    """

    _file_extension = ".json"

    def __init__(self, file_name: str = "uwu"):
        self._file_name = file_name
        self._file_path = self._get_path()

    def get_path_name(self):
        return self._file_path

    def add_airplane(self, airplane: "Airplane"):
        """Метод добавления информации о самолёте в JSON-файл."""
        pass

    def get_airplane(self):
        """Метод получения информации о самолёте из JSON-файла."""
        pass

    def delete_airplane(self, airplane: "Airplane"):
        """Метод удаления информации о самолёте из JSON-файла."""
        pass


if __name__ == '__main__':
    uwu = JSONSaver("uwu")