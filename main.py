from src.airplane import Airplane
from src.api import AirplanesAPI


if __name__ == '__main__':
    api = AirplanesAPI()
    list_ = api.get_airplanes('Canada')
    # print(*list_, sep="\n")

    # Преобразование набора данных в список объектов
    airplanes = Airplane.cast_to_object_list(list_)
    print(*airplanes, sep="\n")

    # Пример работы конструктора класса с одним самолетом
    aeroplane = Airplane("a612a6", "United States", False,100, 10203.18)

    # # Сохранение информации в файл4
    # json_saver = JSONSaver()
    # json_saver.add_aeroplane(vacancy)
    # json_saver.delete_aeroplane(vacancy)
    #
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
