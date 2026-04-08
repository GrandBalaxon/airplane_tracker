import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from src.airplane import Airplane

logger = logging.getLogger("base_saver")


class BaseFileSaver(ABC):
    """Абстрактный базовый класс для сохранения в различные типы файлов."""

    _file_extension = ""

    __slots__ = ["_file_name", "_file_path", "_airplanes_data"]

    _file_name: str
    _file_path: Path
    _airplanes_data: dict[str, dict[str, Any]]

    @abstractmethod
    def _get_airplanes_data_from_file(self) -> None:
        """Абстрактный метод для извлечения данных о самолётах из прикрепленного к объекту класса файла."""
        pass

    @abstractmethod
    def _initialize_file(self) -> None:
        """Абстрактный метод для проверки существования файла и его инициализации при отсутствии."""
        pass

    @abstractmethod
    def _write_airplanes_data_to_file(self) -> None:
        """Абстрактный метод для внесения всех текущих данных из датасета в файл."""
        pass

    @abstractmethod
    def add_airplane(self, airplane: "Airplane") -> None:
        """Абстрактный метод добавления информации о самолёте в файл."""
        pass

    @abstractmethod
    def delete_airplane(self, airplane: "Airplane") -> None:
        """Абстрактный метод удаления информации о самолёте из файла."""
        pass

    @abstractmethod
    def get_airplane(self, airplane_id: str) -> "Airplane | None":
        """Абстрактный метод получения информации о самолёте из файла."""
        pass

    def _get_path(self) -> Path:
        """Метод для получения PATH к рабочему файлу."""
        if self._file_name.endswith(self.__class__._file_extension):
            return Path(__file__).parent.parent / "data" / self._file_name
        else:
            return Path(__file__).parent.parent / "data" / f"{self._file_name}{self.__class__._file_extension}"

    def _is_airplane_in_dataset(self, airplane: "Airplane | str") -> bool | None:
        """
        Метод проверки наличия данных о самолёте в датасете экземпляра класса.

        Если на вход даётся объект класса "Airplane" - то проверяет все его данные.
        При точном совпадении всех данных о борте - возвращает True.

        Если на вход даётся строка с "airplane_id", то проверяется наличие данных о данном самолёте по его ID.
        """
        try:
            if len(self._airplanes_data) == 0:
                file_extension = self.__class__._file_extension[1:].upper()
                logger.info(f"Датасет/{file_extension}-файл пока что пуст.")
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
