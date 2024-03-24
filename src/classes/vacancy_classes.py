from abc import ABC, abstractmethod
import json


class BaseVacancy(ABC):
    """ Абстрактный общий класс для всех вакансий"""

    # Определяем абстрактный метод класса
    @classmethod
    @abstractmethod
    def cast_to_object_list(cls, value):
        pass

    # Определяем абстрактный метод
    @abstractmethod
    def get_name(self):
        pass


class Vacancy(BaseVacancy):
    """ Класс Vacance - дочерний от BaseVacance """

    def __init__(self, name, area, requirement, responsibility, salary, employer, alternate_url):
        """ Метод инициализации экземпляра класса Vacance.
            Задаем значения атрибутам экземпляра.
        """
        self.name = name
        self.area = area
        self.requirement = self.check(requirement)
        self.responsibility = self.check(responsibility)
        self.salary = self.salary_value(salary)
        self.employer = employer
        self.alternate_url = alternate_url
        self.dbg_salary = salary  # оставил для отладки
        super().__init__()

    def __str__(self):
        """
        Строковое отображение атрибутов класса для пользователя
        :return:
        """
        return (f'Наименование вакансии: {self.name}\n'
                f'Место работы: {self.area}\n'
                f'Требования: {self.requirement}\n'
                f'Обязанности: {self.responsibility}\n'
                f'Зарплата: {self.salary}, подробно: {self.dbg_salary}\n'
                f'Работодатель: {self.employer}\n'
                f'Ссылка на вакансию: {self.alternate_url}\n'
                )

    def __repr__(self):
        attrs = ', '.join([f"{attr}={getattr(self, attr)}" for attr in self.__dict__])
        return f"Объект класса: {self.__class__.__name__}. Атрибуты: ({attrs})"

    def __lt__(self, other):
        """ Функция сравнения  вакансий по зарплате """
        return self.salary < other.salary

    def __gt__(self, other):
        """ Функция сравнения  вакансий по зарплате """
        return self.salary > other.salary

    def __eq__(self, other):
        """ Функция сравнения  вакансий по зарплате """
        return self.salary == other.salary

    @classmethod
    def cast_to_object_list(cls, data: list):
        """
        Преобразование набора данных из JSON в список обьектов
        :param data:
        :return: список обьектов класса Vacancy
        """
        vacancies_list = []
        for value in data:
            vacancies_list.append(cls(name=value['name'],
                                      area=value['area'].get('name'),
                                      requirement=value['snippet'].get('requirement'),
                                      responsibility=value['snippet'].get('responsibility'),
                                      salary=value['salary'],
                                      employer=value['employer'].get('name'),
                                      alternate_url=value['alternate_url']
                                      )
                                  )

        if len(vacancies_list) == 0 or vacancies_list is None:
            raise ValueError("Список вакансий не может быть пустым")
        return vacancies_list

    def get_name(self):
        return self.name

    def get_requirement(self):
        return self.requirement

    def get_employer(self):
        return self.employer

    def get_alternate_url(self):
        return self.alternate_url

    @staticmethod
    def without_alfa(st: str):
        """
        Функция извлекает из строки только цифры
        """
        return ''.join(c if c.isdigit() else '' for c in st).strip()

    @staticmethod
    def check(value):
        """
        Проверка значений атрибутов класса на None
        :param value:
        :return:
        """
        if value is None:
            return f'Требования не указаны'
        else:
            return f'{value}'

    def salary_value(self, sl):
        """ Возвращает значение зарплаты после разбора значения sl
            если задан минимальный и максимальный размер - возвращает minimum
        """
        # В случае, если sl - строка с дефисом (100000 - 200000 RUB)
        if isinstance(sl, str) and '-' in sl:
            sl_parts = sl.split('-')
            try:
                return int(''.join(sl_parts[0]))
            except ValueError:
                return 0

        # В случае, если sl - строка с '{' - json-формат?
        elif isinstance(sl, str) and '{' in sl:
            try:
                return json.loads(sl).get('from')
            except ValueError:
                try:
                    return int(self.without_alfa(sl))
                except ValueError:
                    return 0

        # В случае, если sl - строка с пробелами (до 280 000 ₽ на руки)
        elif isinstance(sl, str) and ' ' in sl:
            try:
                return int(self.without_alfa(sl))
            except ValueError:
                return 0

        # В случае, если sl - число в символьном формате
        elif isinstance(sl, str):
            try:
                return int(sl)
            except ValueError:
                return 0

        # В случае, если sl - словарь
        elif isinstance(sl, dict):
            try:
                s_min = sl.get('from')
                s_max = sl.get("to")
                if s_min is not None:
                    return s_min
                elif s_max is not None:
                    return s_max
                else:
                    return 0
            except ValueError:
                return 0

        # В случае, если sl - число
        elif isinstance(sl, int):
            return sl
        else:
            return 0
