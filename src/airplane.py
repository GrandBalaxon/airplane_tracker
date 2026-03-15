import logging
from typing import Any

logger = logging.getLogger("airplane")

class Airplane:
    """Представляет информацию о воздушном судне.

    Attributes:
        callsign (str): Позывной самолёта (например, "UAL1621").
        country (str): Страна регистрации воздушного судна.
        velocity (float): Скорость полёта в м/с.
        geo_altitude (float): Геометрическая высота в метрах.
    """

    __slots__ = ["callsign", "country", "velocity", "geo_altitude"]

    def __init__(self, callsign: str, country: str, velocity: float | int, geo_altitude: float):
        self.callsign = callsign
        self.country = country
        self.velocity = self._validate_velocity(velocity)
        self.geo_altitude = geo_altitude

    @staticmethod
    def _validate_velocity(value: float | int) -> float | None:
        """Приватный метод для валидации скорости."""
        if not isinstance(value, (int, float)):
            logger.warning(f"Скорость должна быть числом, получено {type(value)}")
            return None
        elif value < 90 or value > 1000:
            logger.warning(f"Скорость {value} м/с выходит за пределы допустимого диапазона (90-1000 м/с)")
            return None
        else:
            return value

    @staticmethod
    def cast_to_object_list(states_list: list[list[Any]]) -> list[Airplane]:
        """Метод для преобразования списка со списками данных о самолётах в список объектов класса Airplane."""
        result_list = []

        for state in states_list:
            callsign = state[1]
            country = state[2]
            velocity = state[9]
            geo_altitude = state[13]
            airplane = Airplane(callsign, country, velocity, geo_altitude)

            result_list.append(airplane)

        return result_list