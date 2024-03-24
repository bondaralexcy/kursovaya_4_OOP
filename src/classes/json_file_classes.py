from abc import ABC, abstractmethod
import json
import os
from src.classes.vacancy_classes import Vacancy


class FileManager(ABC):
    """
        Абстрактный класс который обязывает реализовать методы
        для добавления вакансий в файл, получения данных из файла
        по указанным критериям и удаления информации о вакансиях """

    @abstractmethod
    def export_to_file(self, vacancy: Vacancy):
        pass

    @abstractmethod
    def import_from_file(self, keyword):
        pass

    @abstractmethod
    def clear_file(self):
        pass


class JsonFileManager(FileManager):

    def __init__(self, file_worker: str):
        self.file_worker = file_worker

    def export_to_file(self, vacancy):
        """ Добавляем одну вакансию в json-файл"""
        root_dir = os.path.dirname(os.path.dirname(__file__))
        path = os.path.join(root_dir, "../data", self.file_worker)
        with open(path, 'a', encoding='utf-8') as fn:
            # json.dump(vacancy.__dict__, fn)
            json.dump(vacancy, fn)
            fn.write('\n')

    def import_from_file(self, keywords=""):
        """ Загружаем вакансии из json-файла в список vacancies"""
        root_dir = os.path.dirname(os.path.dirname(__file__))
        path = os.path.join(root_dir, "../data", self.file_worker)

        with open(path, 'r', encoding='utf-8') as file:
            vacancies = [json.loads(line) for line in file.readlines()]
        return vacancies

    def clear_file(self):
        """ Очищаем файл перез загрузкой вакансий"""
        root_dir = os.path.dirname(os.path.dirname(__file__))
        path = os.path.join(root_dir, "../data", self.file_worker)
        open(path, 'w').close()
