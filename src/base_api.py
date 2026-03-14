from abc import ABC, abstractmethod

import requests


class BaseAPiClient(ABC):
    """Абстрактный базовый класс для работы с API."""

    @staticmethod
    def _make_request(url: str, params: dict = None, headers: dict = None) -> dict:
        """
        Выполняет GET-запрос к указанному URL с параметрами и заголовками.
        Проверяет статус ответа и возвращает декодированный JSON.
        В случае ошибки выбрасывает исключение.
        """
        response = requests.get(url, params=params, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Ошибка подключения: {response.status_code} - {response.text}")

        return response.json()

    @abstractmethod
    def get_airplanes(self, country: str) -> list:
        """Метод получения списка самолётов в указанной стране."""
        pass