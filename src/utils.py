def filter_vacancies(vacancies_list, filter_words):
    """ Функция для фильтрации вакансий
    :param vacancies_list: список вакансий
    :param filter_words: ключевые слова для фильтра
    :return:
    """
    filtered_vacancies = []

    if not filter_words:
        return vacancies_list

    for vacancy in vacancies_list:
        for keyword in filter_words:
            if (keyword.lower() in vacancy.name.lower()
                    or keyword.lower() in vacancy.area.lower()
                    or keyword.lower() in vacancy.employer.lower()
                    or keyword.lower() in vacancy.requirement.lower()
                    or keyword.lower() in vacancy.responsibility.lower()
            ):
                filtered_vacancies.append(vacancy)

    if len(filtered_vacancies) != 0 or filtered_vacancies is None:
        return filtered_vacancies
    else:
        return [f'Вакансии по заданным критериям не найдены']


def get_vacancies_by_salary(filtered_vacancies, salary_range):
    """
    Функция для отбора и сортировки вакансий по зарплате
    :param filtered_vacancies: список вакансий
    :param salary_range: минимальная зарплата
    :return: ranged_vacancies
    """
    # Если требуемая зарплата не указана,
    # то возвращаем отсортированный исходный список
    if len(salary_range) == 0:
        filtered_vacancies.sort(key=lambda vac: vac.salary, reverse=True)
        return filtered_vacancies

    # Отбираем вакансии по критерию
    ranged_vacancies = []
    for vacancy in filtered_vacancies:
        if int(vacancy.salary) >= int(salary_range):
            ranged_vacancies.append(vacancy)

    if len(ranged_vacancies) == 0 or ranged_vacancies is None:
        return [f'Требуемые вакансии не найдены. Измените запрос']

    # Сортируем по размеру зарплаты
    ranged_vacancies.sort(key=lambda vac: vac.salary, reverse=True)
    return ranged_vacancies


def get_top_vacancies(sorted_vacancies, top_n):
    """
    Функция для получения первых top_n вакансий
    :param sorted_vacancies: список вакансий
    :param top_n: количество топовых вакансий
    :return:
    """
    if len(sorted_vacancies) < top_n:
        top_n = len(sorted_vacancies)

    top_vacancies = sorted_vacancies[:top_n]
    return top_vacancies


def pretty_print(vc_list):
    """ Отладочная печать"""
    i = 0
    for unit in vc_list:
        i += 1
        print(unit)
    print(f'Общее количество отобранных вакансий = {i}')
