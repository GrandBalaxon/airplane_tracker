import logging
from abc import ABC, abstractmethod
from typing import Any, cast

import requests

logger = logging.getLogger("base_api")


class BaseAPIClient(ABC):
    """Абстрактный базовый класс для работы с API."""

    @staticmethod
    def _make_request(
            url: str,
            params: dict[str, Any] | None = None,
            headers: dict[str, Any] | None = None,
    ) -> Any:
        """
        Выполняет GET-запрос к указанному URL с параметрами и заголовками.
        Проверяет статус ответа и возвращает декодированный JSON.
        В случае ошибки выбрасывает исключение.
        """
        response = requests.get(url, params=params, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Ошибка подключения: {response.status_code} - {response.text}")

        return cast(dict[str, Any], response.json())

    @abstractmethod
    def get_airplanes(self, country: str) -> list[list[Any]]:
        """Метод получения списка самолётов в указанной стране."""
        pass
