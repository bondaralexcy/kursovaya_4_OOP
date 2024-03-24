import os
import os.path
import pytest
from src.classes.json_file_classes import JsonFileManager
from src.classes.api_classes import ConnectAPI


@pytest.fixture
def json_manager():
    return JsonFileManager('test_vacancies.json')


def test_export_to_file(json_manager):
    hh_api = ConnectAPI()
    vc_list = hh_api.get_vacancies("")
    for vacancy in vc_list:
        json_manager.export_to_file(vacancy)

    vac_list = json_manager.import_from_file()

    assert len(vac_list) == 100
    assert vac_list[0]['area'].get("name") == 'Москва'


def test_clear_file(json_manager):
    json_manager.clear_file()
    vacancies = json_manager.import_from_file()
    root_dir = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(root_dir, "data", 'test_vacancies.json')

    assert len(vacancies) == 0
    assert os.path.exists(path)

    os.remove(path)
