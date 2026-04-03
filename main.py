from src.airplane import Airplane
from src.api import AirplanesAPI
from src.csv_saver import CSVSaver
from src.json_saver import JSONSaver

if __name__ == '__main__':
    # api = AirplanesAPI()
    # list_ = api.get_airplanes('Ukraine')
    # # print(*list_, sep="\n")

    # # Преобразование набора данных в список объектов
    # airplanes = Airplane.cast_to_object_list(list_)
    # print(*sorted(airplanes), sep="\n")

    # Пример работы конструктора класса с одним самолетом
    aeroplane_1 = Airplane("a612a6", "United States", False,100, 10203.18)
    aeroplane_2 = Airplane("a612a7", "United States", False, 100, 9203.18)

    # Сохранение информации в файл JSON
    json_saver = JSONSaver()

    json_saver.add_airplane(aeroplane_1)
    json_saver.add_airplane(aeroplane_2)
    json_saver.delete_airplane(aeroplane_1)
    json_saver.delete_airplane("a851")

    aeroplane_3 = json_saver.get_airplane("a612a7")

    # Сохранение информации в файл CSV
    csv_saver = CSVSaver()

    csv_saver.add_airplane(aeroplane_1)
    csv_saver.add_airplane(aeroplane_2)
    csv_saver.add_airplane(aeroplane_3)
    csv_saver.delete_airplane(aeroplane_1)

    aeroplane_4 = csv_saver.get_airplane("a612a7")

    # # Функция для взаимодействия с пользователем
    # def user_interaction():
    #     country = input("Введите название страны: ")
    #     top_n = int(input("Введите количество самолетов для вывода в топ N: "))
    #     filter_words = input("Введите названия стран для фильтрации по стране регистрации: ").split()
    #     altitude_range = input("Введите диапазон высот полета: ") # Пример: 100000 - 150000
    #
    #     filtered_aeroplanes = filter_aeroplanes(aeroplanes, filter_words)
    #
    #     ranged_aeroplanes = get_aeroplanes_by_altitude(aeroplanes, altitude_range)
    #
    #     sorted_aeroplanes = sort_aeroplanes(ranged_aeroplanes)
    #     top_aeroplanes = get_top_aeroplanes(sorted_aeroplanes, top_n)
    #     print_aeroplanes(top_aeroplanes)