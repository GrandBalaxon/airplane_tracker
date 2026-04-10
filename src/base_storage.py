from abc import ABC, abstractmethod


class BaseStorage(ABC):
    """Абстрактный базовый класс для сохранения в различные типы файлов."""

    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def save(self):
        pass
