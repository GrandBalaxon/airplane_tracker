import logging
from typing import Any

from src.airplane import Airplane
from src.base_storage import BaseStorage

logger = logging.getLogger("airplane_service")


class AirplaneService:
    """Класс для работы с информацией о самолётах (объектах класса Airplane).

    Attributes:
        _storage (BaseStorage): Хранилище экземпляра класса
        _airplanes_data (dict): Датасет с данными о всех текущих самолётах в хранилище экземпляра класса.
    """

    def __init__(self, storage: BaseStorage):
        self._storage = storage
        self._airplanes_data = storage.load()

    def _is_airplane_in_dataset(self, airplane: "Airplane | str") -> bool | None:
        """
        Метод проверки наличия данных о самолёте в датасете экземпляра класса.

        Если на вход даётся объект класса "Airplane" - то проверяет все его данные.
        При точном совпадении всех данных о борте - возвращает True.

        Если на вход даётся строка с "airplane_id", то проверяется наличие данных о данном самолёте по его ID.
        """
        try:
            if len(self._airplanes_data) == 0:
                logger.info(f"Датасет пока что пуст.")
                return False
            else:
                if isinstance(airplane, Airplane):
                    id_key = airplane.airplane_id

                    if id_key in self._airplanes_data:
                        if (
                            self._airplanes_data[id_key]["country"] == airplane.country
                            and self._airplanes_data[id_key]["on_ground"] == airplane.on_ground
                            and self._airplanes_data[id_key]["velocity"] == airplane.velocity
                            and self._airplanes_data[id_key]["geo_altitude"] == airplane.geo_altitude
                        ):
                            return True
                        else:
                            return False
                    else:
                        return False

                elif isinstance(airplane, str):
                    if airplane in self._airplanes_data:
                        return True
                    else:
                        return False

                else:
                    raise TypeError(f"Неверный формат {type(airplane)}, ожидается объект класса Airplane или str.")

        except Exception as e:
            logger.error(f"Непредвиденная ошибка: {e}")
            raise

    def _add_airplane_to_dataset(self, airplane: "Airplane") -> None:
        """Метод для добавления данных в датасет экземпляра класса."""
        id_key = airplane.airplane_id
        airplane_data = {
            "country": airplane.country,
            "on_ground": airplane.on_ground,
            "geo_altitude": airplane.geo_altitude,
            "velocity": airplane.velocity,
        }
        self._airplanes_data[id_key] = airplane_data

    def _delete_airplane_from_dataset(self, id_key: str) -> None:
        """Метод удаления данных о самолёте из датасета."""
        del self._airplanes_data[id_key]

    def get_airplanes_amount(self) -> int:
        """Геттер выдающий текущее количество самолетов в датасете/файле экземпляра класса."""
        if len(self._airplanes_data) > 0:
            return len(self._airplanes_data)
        else:
            return 0

    def add_airplane(self, airplane: "Airplane") -> None:
        """Метод добавления информации о самолёте в JSON-файл."""
        try:
            if self._is_airplane_in_dataset(airplane):
                logger.info(f"Данные о борте {airplane.airplane_id} уже записаны.")
            else:
                self._add_airplane_to_dataset(airplane)
                self._storage.save()

                logger.debug(f"Данные о борте {airplane.airplane_id} записаны в файл.")

        except Exception as e:
            logger.error(f"Возникла ошибка: {e}")
            raise

    def delete_airplane(self, airplane: "Airplane | str") -> None:
        """Метод удаления информации о самолёте из JSON-файла."""
        try:
            id_key = airplane.airplane_id if isinstance(airplane, Airplane) else airplane
            if self._is_airplane_in_dataset(airplane):
                logger.info(f"Данные о борте {id_key} найдены в файле.")

                self._delete_airplane_from_dataset(id_key)
                self._storage.save()

                logger.info(f"Данные о борте {id_key} удалены из файла.")

            else:
                logger.info(f"Данные о борте {id_key} не найдены в файле.")

        except Exception as e:
            logger.error(f"Возникла ошибка: {e}")
            raise

    def get_airplane(self, airplane_id: str | Any) -> "Airplane | None":
        """Метод получения информации о самолёте из JSON-файла.

        Args:
            airplane_id (str): Уникальный идентификационный номер самолета по ИКАО, отображаемый в шестнадцатеричном
                формате, как он установлен в транспондере самолета (может быть неверным, пример номера "a50e93")
        """
        try:
            if not isinstance(airplane_id, str):
                logger.warning(f"Неверный формат ID самолёта: {type(airplane_id)}.")
                return None
            else:
                if self._is_airplane_in_dataset(airplane_id):

                    airplane_data = self._airplanes_data.get(airplane_id)
                    if airplane_data is None:
                        return None

                    logger.info(f"Возвращение данных о борте {airplane_id} из JSON-файла.")
                    return Airplane(aircraft_id=airplane_id, **airplane_data)

                else:
                    logger.warning(f"Данных о борте {airplane_id} не найдено в JSON-файле.")
                    return None

        except Exception as e:
            logger.error(f"Возникла ошибка: {e}")
            raise
