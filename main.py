
from src.classes.api_classes import ConnectAPI
from src.classes.json_file_classes import JsonFileManager
from src.classes.vacancy_classes import Vacancy
from src.utils import filter_vacancies, get_top_vacancies, get_vacancies_by_salary

VACANCIES_FILE = "vacancies.json"


def user_interactions():
    """ Функция для взаимодействия с пользователем.
    Функция должна взаимодействовать с пользователем через консоль.
    Возможности этой функции должны быть следующими:
    ввести поисковый запрос для запроса вакансий из hh.ru;
    получить топ N вакансий по зарплате (N запрашивать у пользователя);
    получить вакансии с ключевым словом в описании.
    """

    # Создание экземпляра класса для работы с API сайтов с вакансиями
    hh_api = ConnectAPI()

    print('Поиск вакансий будет проводиться по московским работодателям!')
    # Запрашиваем ключевое слово для загрузки вакансий с API-сервиса
    keyword = str(input("Введите строку поиска: "))    # Например: python

    # Получение вакансий с hh.ru в формате JSON с ключевым словом keyword
    # и преобразование набора данных из JSON в список вакансий
    vc_list = hh_api.get_vacancies(keyword)
    if vc_list is None:
        print('Сервис hh.ru не отработал.')
        print('Попробуйте позже.')
        exit()

    # Создаем экземпляр класса для действий с вакансиями в JSON-файле
    jfm = JsonFileManager(VACANCIES_FILE)
    # Очищаем json-файл и записываем в него полученные данные
    jfm.clear_file()
    for vacancy in vc_list:
        jfm.export_to_file(vacancy)

    # Импортируем вакасии из файла в список JSON-формата
    data = jfm.import_from_file()
    # Преобразование набора данных из JSON-формата в список объектов
    vacancies_list = Vacancy.cast_to_object_list(data)

    # Фильтрация вакансий по ключевым словам
    filter_words = input("Введите ключевые слова через запятую: ").lower().split()    # Например: junior, middle

    filtered_vacancies = filter_vacancies(vacancies_list, filter_words)

    # Фильтрация и ранжирование по размеру зарплаты
    salary_range = input("Введите минимально допустимую зарплату: ")  # Пример: 100000
    ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)

    # Выводим топ N вакансий
    try:
        top_n = int(input("Введите количество вакансий для вывода на консоль (по умолчанию 20): "))
    except ValueError:
        top_n = 20

    if top_n > 0:
        # Отбор N первых вакансий
        top_vacancies = get_top_vacancies(ranged_vacancies, top_n)
        # Вывод на консоль
        for idx, vacancy in enumerate(top_vacancies, start=1):
            print(f"\n{idx}. {vacancy}")

    # Завершение работы с вакансиями
    res = input("Продолжить работу (Y/N)?")
    if res.upper() == 'Y':
        user_interactions()
    exit()


if __name__ == '__main__':
    user_interactions()

