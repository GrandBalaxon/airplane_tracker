from abc import ABC, abstractmethod
from typing import Any


class BaseAPIClient(ABC):
    """Абстрактный базовый класс для работы с API."""

    @abstractmethod
    def get_airplanes(self, country: str) -> list[list[Any]]:
        """Метод получения списка самолётов в указанной стране."""
        pass
