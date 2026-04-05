import logging
from typing import Any, Optional

logger = logging.getLogger("airplane")


class Airplane:
    """Класс представляющий информацию о воздушном судне.

    Attributes:
        airplane_id (str): Уникальный идентификационный номер самолета по ИКАО, отображаемый в шестнадцатеричном
            формате, как он установлен в транспондере самолета (может быть неверным, пример номера "a50e93")
        country (str): Страна регистрации воздушного судна
        on_ground (bool): Флаг нахождения самолёта на земле
        velocity (Optional[float]): Скорость полёта в м/с
        geo_altitude (Optional[float]): Геометрическая высота в метрах
    """

    __slots__ = ["airplane_id", "country", "on_ground", "velocity", "geo_altitude"]

    def __init__(
        self,
        aircraft_id: str,
        country: str,
        on_ground: bool,
        velocity: Optional[float],
        geo_altitude: Optional[float],
    ) -> None:

        self.airplane_id = self._validate_aircraft_id(aircraft_id)
        self.country = self._validate_country(country)
        self.on_ground = self._validate_on_ground_status(on_ground)
        self.geo_altitude = self._validate_altitude(geo_altitude)
        self.velocity = self._validate_velocity(velocity)

    def __repr__(self) -> str:
        return (
            f"Airplane (icao_id = {self.airplane_id}, country = {self.country}, "
            f"on_ground = {self.on_ground}, velocity = {self.velocity}, geo_altitude = {self.geo_altitude})"
        )

    def __str__(self) -> str:
        """Переопределенный метод для отображения str экземпляра класса."""
        velocity_str = f"{self.velocity} м/c" if self.velocity else "0"
        altitude_str = f"{self.geo_altitude} м" if self.geo_altitude else "на земле"
        return f"Борт {self.airplane_id} - {self.country} (Скорость: {velocity_str}, Высота: {altitude_str})"

    @staticmethod
    def _validate_aircraft_id(value: str | int) -> str:
        """Приватный метод для валидации идентификатор борта."""
        if not isinstance(value, (str, int)):
            raise ValueError(f"Идентификатор борта должен быть строкой, получено {type(value)}")
        else:
            if isinstance(value, int):
                logger.debug("Получено и обработано численное значение ID самолёта.")
                return str(value)
            else:
                return value.strip()

    @staticmethod
    def _validate_country(value: str) -> str:
        """Приватный метод для валидации страны регистрации самолёта."""
        if not isinstance(value, str):
            logger.warning(f"Название страны должно быть строкой, получено {value} класса {type(value)}")
            return ""
        else:
            return value.strip()

    @staticmethod
    def _validate_on_ground_status(value: bool | str) -> bool:
        """Приватный метод для валидации атрибута on_ground."""
        if isinstance(value, str):
            value = value.lower().strip()
            if value == "true":
                return True
            elif value == "false":
                return False
            else:
                info = f"Флаг 'on_ground' должен быть True/False, получено: {value}"
                raise ValueError(info)
        elif isinstance(value, bool):
            return value
        else:
            info = f"Флаг 'on_ground' должен быть True/False, получено: {value} класса {type(value)}."
            raise ValueError(info)

    def _validate_altitude(self, value: Optional[float | int]) -> Optional[float]:
        """Приватный метод для валидация высоты (должна быть числом в разумных пределах от 0 до 20000 м.)"""

        if isinstance(value, (int, float)):
            if value < -400 or value > 40000:
                info = f"Борт {self.airplane_id} - {self.country}: высота {value} м выходит за пределы допустимого диапазона (-400 – 40000 м)"
                raise ValueError(info)
            else:
                return float(value)

        elif value is None:
            if not self.on_ground:
                info = f"Борт {self.airplane_id} - {self.country} сейчас на земле, но имеет знач. высоты {value}."
                raise ValueError(info)
            else:
                return 0

        else:
            info = f"Высота должна быть числом или None, получено {type(value)}"
            raise TypeError(info)

    def _validate_velocity(self, value: float | int) -> float:
        """Приватный метод для валидации скорости."""

        if isinstance(value, (int, float)):
            if value < 0 or value > 1000:
                info = f"Борт {self.airplane_id} - {self.country}: Скорость {value} м/с за пределами диапазона (0-1000 м/с)"
                raise ValueError(info)
            else:
                return float(value)

        elif value is None:
            if not self.on_ground:
                info = f"Самолёт id[{self.airplane_id}] не на земле, но не имеет скорости полёта."
                raise ValueError(info)
            else:
                return 0

        else:
            info = f"Скорость должна быть числом или None, получено {type(value)}"
            raise TypeError(info)

    def __lt__(self, other: "Airplane") -> bool:
        """Метод для логического сравнения 'меньше чем'."""
        if not isinstance(other, Airplane):
            raise TypeError(f"Ошибка: сравнение с некорректным типом {type(other)}.")
        elif self.geo_altitude == other.geo_altitude:
            return self.velocity < other.velocity
        else:
            return self.geo_altitude < other.geo_altitude

    def __le__(self, other: "Airplane") -> bool:
        """Метод для логического сравнения 'меньше или равно'."""
        if not isinstance(other, Airplane):
            raise TypeError(f"Ошибка: сравнение с некорректным типом {type(other)}.")
        elif self.geo_altitude == other.geo_altitude:
            return self.velocity <= other.velocity
        else:
            return self.geo_altitude <= other.geo_altitude

    def __gt__(self, other: "Airplane") -> bool:
        """Метод для логического сравнения 'больше чем'."""
        if not isinstance(other, Airplane):
            raise TypeError(f"Ошибка: сравнение с некорректным типом {type(other)}.")
        elif self.geo_altitude == other.geo_altitude:
            return self.velocity > other.velocity
        else:
            return self.geo_altitude > other.geo_altitude

    def __ge__(self, other: "Airplane") -> bool:
        """Метод для логического сравнения 'больше или равно'."""
        if not isinstance(other, Airplane):
            raise TypeError(f"Ошибка: сравнение с некорректным типом {type(other)}.")
        elif self.geo_altitude == other.geo_altitude:
            return self.velocity >= other.velocity
        else:
            return self.geo_altitude >= other.geo_altitude

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

            try:
                aircraft = Airplane(aircraft_id, country, on_ground, velocity, geo_altitude)
            except Exception as e:
                logger.debug(f"Не прошел проверку: {state}")
                logger.error(e)
                continue
            else:
                result_list.append(aircraft)

        logger.info(f"Данных валидировано: {len(result_list)}/{len(states_list)}.")
        return result_list
