from abc import ABC, abstractmethod
from pathlib import Path

from src.base_storage import BaseStorage


class FileStorage(BaseStorage, ABC):
    """Абстрактный базовый класс для работы с различными типами файлов в виде хранилища.

    Attributes:
        _file_name (str): Имя файла-хранилища экземпляра класса.
        _file_path (Path): PATH к рабочему файлу-хранилищу экземпляра класса.
    """

    _file_extension = ""

    __slots__ = ["_file_name", "_file_path"]

    _file_name: str
    _file_path: Path

    def __init__(self, file_name: str | None = None):
        if file_name:
            self._file_name = file_name
        else:
            self._file_name = self._default_file_name()

        self._file_path: Path = self._get_path()
        self._initialize_file()

    @abstractmethod
    def _default_file_name(self) -> str:
        """Дефолтное имя файла для конкретного storage."""
        pass

    @abstractmethod
    def _initialize_file(self) -> None:
        """Абстрактный метод для проверки существования файла и его инициализации при отсутствии."""
        pass

    def _get_path(self) -> Path:
        """Метод для получения PATH к рабочему файлу."""
        if self._file_name.endswith(self.__class__._file_extension):
            return Path(__file__).parent.parent / "data" / self._file_name
        else:
            return Path(__file__).parent.parent / "data" / f"{self._file_name}{self.__class__._file_extension}"
