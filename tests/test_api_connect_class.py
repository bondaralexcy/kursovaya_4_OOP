import pytest
from src.classes.api_classes import ConnectAPI


@pytest.fixture
def api_instance():
    """
        Создаем экземпляр класса ConnectAPI для тестирования
    """
    return ConnectAPI()


def test_get_vacancies(api_instance):
    key_word = 'python'
    vacancies = api_instance.get_vacancies(key_word)
    assert isinstance(vacancies, list)
