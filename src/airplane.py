import logging
from typing import Any, Optional

logger = logging.getLogger("airplane")


class Airplane:
    """Представляет информацию о воздушном судне.

    Attributes:
        callsign (str): Позывной самолёта (например, "UAL1621").
        country (str): Страна регистрации воздушного судна.
        velocity (float): Скорость полёта в м/с.
        geo_altitude (float): Геометрическая высота в метрах.
    """

    __slots__ = ["callsign", "country", "on_ground", "velocity", "geo_altitude"]

    def __init__(
        self, callsign: str, country: str, on_ground: bool, velocity: float, geo_altitude: Optional[float]
    ) -> None:
        self.callsign = callsign
        self.country = country
        self.on_ground = on_ground
        self.velocity = velocity
        self.geo_altitude = geo_altitude

    def __str__(self):
        return f"{self.callsign} (Страна: {self.country}, Скорость: {self.velocity}, Высота: {self.geo_altitude})"

    @staticmethod
    def _validate_callsign(value: str) -> Optional[str]:
        """Приватный метод для валидации позывного рейса."""
        if not isinstance(value, str):
            logger.error(f"Позывной борта должен быть строкой, получено {type(value)}")
            return None
        elif value.strip() == "":
            logger.error(f"Позывной борта должен быть не пустой строкой.")
            return None
        else:
            return value.strip()

    def _validate_altitude(self, value: float | int) -> Optional[float]:
        """Валидация высоты: должна быть числом в разумных пределах (например, -1000 … 30000 м)."""
        if not isinstance(value, (int, float)):
            logger.error(f"Высота должна быть числом, получено {type(value)}")
            return None
        if value < 0 or value > 20000:
            logger.warning(f"Высота {value} м выходит за пределы допустимого диапазона (-1000–30000 м)")
            return None
        elif self.on_ground and not value:
            logger.warning(
                f"Самолёт {self.callsign, self.country} стоит на земле и при этом имеет не корректное значение высоты."
            )
            return None
        return float(value)

    def _validate_velocity(self, value: float | int) -> Optional[float]:
        """Приватный метод для валидации скорости."""
        if not isinstance(value, (int, float)):
            logger.error(f"Скорость должна быть числом, получено {type(value)}")
            return None
        elif value < 90 or value > 1000:
            logger.warning(f"Скорость {value} м/с выходит за пределы допустимого диапазона (90-1000 м/с)")
            return None
        else:
            return float(value)

    @classmethod
    def cast_to_object_list(cls, states_list: list[list[Any]]) -> list[Airplane]:
        """Метод для преобразования списка со списками данных о самолётах в список объектов класса Airplane."""
        result_list = []

        for state in states_list:
            callsign = cls._validate_callsign(state[1])
            country = state[2]
            on_ground = state[8]
            velocity = state[9]
            geo_altitude = state[13]

            if callsign and country and on_ground and velocity and geo_altitude:
                airplane = cls(callsign, country, on_ground, velocity, geo_altitude)

            result_list.append(airplane)

        return result_list
