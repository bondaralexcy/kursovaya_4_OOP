import pytest
from src.classes.vacancy_classes import Vacancy


@pytest.fixture
def test_vacancy():
    vacancies = [Vacancy("Title", "1", "requirement", "responsibility",
                {"from": 130000, "to": 140000, "currency": "RUR", "gross": False},
                "employer", "hh.ru"),
                Vacancy("Title1", "1", "requirement1", "responsibility1",
                {"from": 130000, "to": 140000, "currency": "RUR", "gross": False},
                "employer1", "hh.ru"),
                Vacancy("Title2", "1", "requirement2", "responsibility2",
                {"from": None, "to": 140000, "currency": "RUR", "gross": False},
                "employer2", "hh.ru")
                 ]
    return vacancies


def test_init_vacancy(test_vacancy):
    vacancy_1 = test_vacancy[1]
    assert vacancy_1.name == 'Title1'

    vacancy_2 = test_vacancy[2]
    assert vacancy_2.requirement == "requirement2"


def test_salary_value(test_vacancy):
    vacancy_1 = test_vacancy[1]
    assert vacancy_1.salary_value(vacancy_1.salary) == 130000

    vacancy_2 = test_vacancy[2]
    assert vacancy_2.salary == 140000
