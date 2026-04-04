from datetime import datetime

from src.airplane import Airplane
from src.api import AirplanesAPI
from src.csv_saver import CSVSaver
from src.json_saver import JSONSaver


def generate_filename(country: str, extension: str) -> str:
    now = datetime.now()
    return (
        f"{country}_"
        f"{now.day:02d}_{now.month:02d}_{now.year}_"
        f"{now.hour:02d}_{now.minute:02d}."
        f"{extension.lower()}"
    )

def create_saver(country: str, airplanes: list[Airplane]) -> None:
    """Функция для выбора расширения файла для сохранения базы данных с самолётами и создания saver объекта."""
    while True:
        file_extension = input("Выберите формат файла для сохранения (JSON/CSV): ").upper()
        if file_extension == "JSON":
            file_name = input("Введите имя файла (или Enter): ")
            if file_name == "":
                json_saver = JSONSaver(generate_filename(country, file_extension))
            else:
                json_saver = JSONSaver(file_name)
            for data in airplanes:
                json_saver.add_airplane(data)
            break
        elif file_extension == "CSV":
            file_name = input("Введите имя файла (или Enter): ")
            if file_name == "":
                csv_saver = CSVSaver(generate_filename(country, file_extension))
            else:
                csv_saver = CSVSaver(file_name)
            for data in airplanes:
                csv_saver.add_airplane(data)
            break
        else:
            print("Указан не верный формат.")

def user_interaction() -> None:
    """Функция для взаимодействия с пользователем."""
    country = input("Введите название страны: ")

    api = AirplanesAPI()
    airplanes_raw_data = api.get_airplanes(country)
    airplanes = Airplane.cast_to_object_list(airplanes_raw_data)

    create_saver(country, airplanes)

    top_n = int(input("Введите количество самолетов для вывода в топ N: "))
    filter_words = input("Введите названия стран для фильтрации по стране регистрации: ").split()
    altitude_range = input("Введите диапазон высот полета: ")  # Пример: 100000 - 150000

    filtered_aeroplanes = filter_aeroplanes(airplanes, filter_words)

    ranged_aeroplanes = get_aeroplanes_by_altitude(airplanes, altitude_range)

    sorted_aeroplanes = sort_aeroplanes(ranged_aeroplanes)
    top_aeroplanes = get_top_aeroplanes(sorted_aeroplanes, top_n)
    print_aeroplanes(top_aeroplanes)

if __name__ == '__main__':
    # Пример работы конструктора класса с одним самолетом
    aeroplane_1 = Airplane("a612a6", "United States", False,100, 10203.18)
    aeroplane_2 = Airplane("a612a7", "United States", False, 100, 9203.18)

    user_interaction()

