import logging
from typing import Any, Optional

logger = logging.getLogger("airplane")


class Airplane:
    """Представляет информацию о воздушном судне.

    Attributes:
        aircraft_id (str): Уникальный идентификатор борта (например, "a50e93").
        country (str): Страна регистрации воздушного судна.
        velocity (float): Скорость полёта в м/с.
        geo_altitude (float): Геометрическая высота в метрах.
    """

    __slots__ = ["aircraft_id", "country", "on_ground", "velocity", "geo_altitude"]

    def __init__(
        self,
        aircraft_id: str,
        country: str,
        on_ground: bool,
        velocity: float,
        geo_altitude: Optional[float],
    ) -> None:
        self.aircraft_id = self._validate_aircraft_id(aircraft_id)
        self.country = country
        self.on_ground = on_ground
        self.velocity = velocity
        self.geo_altitude = geo_altitude

    def __str__(self):
        return f"id[{self.aircraft_id}] (Страна: {self.country}, В полёте: {not self.on_ground}, Скорость: {self.velocity}, Высота: {self.geo_altitude})"

    @staticmethod
    def _validate_aircraft_id(value: str) -> Optional[str]:
        """Приватный метод для валидации идентификатор борта."""
        if not isinstance(value, str):
            logger.error(f"Идентификатор борта должен быть строкой, получено {type(value)}")
            raise ValueError
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
            aircraft_id = state[0]
            country = state[2]
            on_ground = state[8]
            velocity = state[9]
            geo_altitude = state[13]

            if aircraft_id and country and velocity:
                airplane = cls(aircraft_id, country, on_ground, velocity, geo_altitude)

                result_list.append(airplane)

        return result_list
