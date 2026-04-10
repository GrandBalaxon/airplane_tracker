import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from src.airplane import Airplane

logger = logging.getLogger("base_saver")


class BaseStorage(ABC):
    """Абстрактный базовый класс для сохранения в различные типы файлов."""

    _file_extension = ""

    __slots__ = ["_file_name", "_file_path", "_airplanes_data"]

    _file_name: str
    _file_path: Path
    _airplanes_data: dict[str, dict[str, Any]]

    @abstractmethod
    def _get_airplanes_data_from_file(self) -> None:
        """Абстрактный метод для извлечения данных о самолётах из прикрепленного к объекту класса файла."""
        pass

    @abstractmethod
    def _initialize_file(self) -> None:
        """Абстрактный метод для проверки существования файла и его инициализации при отсутствии."""
        pass

    @abstractmethod
    def _write_airplanes_data_to_file(self) -> None:
        """Абстрактный метод для внесения всех текущих данных из датасета в файл."""
        pass

    def _get_path(self) -> Path:
        """Метод для получения PATH к рабочему файлу."""
        if self._file_name.endswith(self.__class__._file_extension):
            return Path(__file__).parent.parent / "data" / self._file_name
        else:
            return Path(__file__).parent.parent / "data" / f"{self._file_name}{self.__class__._file_extension}"
