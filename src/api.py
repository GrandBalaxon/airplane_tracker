import logging
from typing import Any

from .base_api import BaseAPIClient

logger = logging.getLogger("api")


class AirplanesAPI(BaseAPIClient):

    def __init__(self) -> None:
        self._nominatim_url = "https://nominatim.openstreetmap.org/search"
        self._opensky_url = "https://opensky-network.org/api/states/all?"

    def _get_country_bbox(self, country: str) -> list[str]:
        """Приватный метод: получает bounding box страны через Nominatim."""
        params = {
            "country": country,
            "format": "json",
            "limit": 1,
        }
        headers = {"User-Agent": "airplane-tracker-test-app"}
        data = self._make_request(self._nominatim_url, params=params, headers=headers)

        if not data:
            raise ValueError(f"Некорректно указанная страна - {country}, полученная bbox пуста.")
        else:
            bbox: list[str] = data[0]["boundingbox"]
            logger.info(f"Данные о bbox получены: {bbox}")

            return bbox

    def _get_airplanes_states(self, bbox: list[str]) -> dict[str, Any]:
        """Приватный метод: получает состояния самолётов в заданном bounding box через OpenSky."""
        params = {"lamin": bbox[0], "lamax": bbox[1], "lomin": bbox[2], "lomax": bbox[3]}
        data = self._make_request(self._opensky_url, params=params)
        logger.info("Данные успешно загружены.")

        return data

    def get_airplanes(self, country: str) -> list[list[Any]]:
        """Метод, что возвращает список самолётов и их данные для указанной страны."""
        logger.info(f"Попытка получить данные о воздушных судах над '{country}'.")
        bbox = self._get_country_bbox(country)
        states_data = self._get_airplanes_states(bbox)

        result = states_data.get("states", [])
        if result:
            logger.info(f"Получены данные с {len(result)} самолётов.")
        else:
            logger.warning("Отсутствуют воздушные суда в указанной стране.")

        return result
