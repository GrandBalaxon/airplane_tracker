from abc import ABC, abstractmethod
from pathlib import Path

from src.airplane import Airplane


class BaseFileSaver(ABC):
    """Абстрактный базовый класс для сохранения в различные типы файлов."""

    _file_extension = ""

    __slots__ = ["_file_name", "_file_path"]

    def _get_path(self) -> Path:
        """Метод для получения PATH к рабочему файлу."""
        if self._file_name.endswith(self.__class__._file_extension):
            return Path(__file__).parent.parent / "data" / self._file_name
        else:
            return Path(__file__).parent.parent / "data" / f"{self._file_name}{self.__class__._file_extension}"

    @abstractmethod
    def add_airplane(self, airplane: "Airplane") -> None:
        """Абстрактный метод добавления информации о самолёте в файл."""
        pass

    @abstractmethod
    def delete_airplane(self, airplane: "Airplane") -> None:
        """Абстрактный метод удаления информации о самолёте из файла."""
        pass

    def get_airplane(self, airplane_id: str) -> "Airplane":
        """Абстрактный метод получения информации о самолёте из файла."""
        pass
