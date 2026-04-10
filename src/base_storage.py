from abc import ABC, abstractmethod
from typing import Any


class BaseStorage(ABC):
    """Абстрактный базовый класс для сохранения в различные типы файлов."""

    @abstractmethod
    def load(self) -> dict[str, Any]:
        """Абстрактный метод для выгрузки данных из хранилища."""
        pass

    @abstractmethod
    def save(self, data: dict[str, Any]) -> None:
        """Абстрактный метод для загрузки данных в хранилище."""
        pass
