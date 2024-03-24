from abc import ABC, abstractmethod
import json
import requests


class AbstractAPIWorker(ABC):
    """ Абстрактный класс для работы с API сервиса с вакансиями"""

    @abstractmethod
    def get_vacancies(self, key_word):
        pass


class ConnectAPI(AbstractAPIWorker):
    """
        Класс, наследующийся от абстрактного класса, для работы с платформой hh.ru
    """

    def __init__(self) -> None:
        """
        Запрашиваются вакансии, содержащие в поле 'name' текст 'text'
        и только те, в которых указана зарплата
        Поиск ощуществляется по вакансиям Москвы
        """
        self.url = 'https://api.hh.ru/vacancies'
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {'text': '',
                       # 'search_field': 'name',
                       'area': '1',  # Поиск ощуществляется по вакансиям Москвы (код = 1)
                       'only_with_salary': 'true',  # Ищутся только те, в которых указана зарплата
                       'page': 0,
                       'per_page': 100
                       }

    def __repr__(self):
        attrs = ', '.join([f"{attr}={getattr(self, attr)}" for attr in self.__dict__])
        return f"Объект класса: {self.__class__.__name__}. Атрибуты: ({attrs})"

    def get_vacancies(self, keyword: str) -> list:
        """
        Получать список вакансий от сервиса API
        """
        self.params['text'] = keyword

        req = requests.get(self.url, headers=self.headers, params=self.params)  # Посылаем запрос к API
        data = req.content.decode()  # Декодируем его ответ, чтобы Кириллица отображалась корректно
        req.close()
        # Преобразуем данные из json-формата в словарь python
        dict_from_json = json.loads(data)
        value = dict_from_json.get('items')
        return value
