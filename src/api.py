from pprint import pprint

from base_api import BaseAPiClient


class AirplanesAPI(BaseAPiClient):

    def __init__(self) -> None:
        self._nominatim_url = 'https://nominatim.openstreetmap.org/search'
        self._opensky_url = 'https://opensky-network.org/api/states/all?'

    def _get_country_bbox(self, country: str) -> list:
        """"""
        params = {
            'country': country,
            'format': 'json',
            'limit': 1,
        }
        headers = {'User-Agent': 'airplane-tracker-test-app'}
        data = self._make_request(self._nominatim_url, params=params, headers=headers)

        return data[0]['boundingbox']

    def _get_airplanes_states(self, bbox: list) -> dict:
        """"""
        params = {
            "lamin": bbox[0],
            "lamax": bbox[1],
            "lomin": bbox[2],
            "lomax": bbox[3]
        }
        return self._make_request(self._opensky_url, params=params)

    def get_airplanes(self, country: str) -> list:
        """"""
        bbox = self._get_country_bbox(country)
        states_data = self._get_airplanes_states(bbox)
        return states_data.get("states", [])


if __name__ == '__main__':
    api = AirplanesAPI()
    list_ = api.get_airplanes('Russia')
    pprint(list_)