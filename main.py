from classes import HeadHunterAPI, SuperJobAPI, Vacancy, Connector

def main():
    vacancies_json = []
    keyword = "Python"

    """Создание экземпляров класса для работы с API сайтов с вакансиями"""
    hh = HeadHunterAPI(keyword)
    sj = SuperJobAPI(keyword)

    """Получение вакансий с разных платформ"""
    # hh_vacancies = hh.get_request()
    # print(hh_vacancies)
    # hh_vacancies = hh.get_vacancies()
    # print(hh_vacancies)
    # hh_vacancies = hh.get_formatted_vacancies()
    # print(hh_vacancies)
    # sj_vacancies = sj.get_request()
    # sj_vacancies = sj.get_vacancies()
    # sj_vacancies = sj.get_formatted_vacancies()
    # print(sj_vacancies)

    for api in (hh, sj):
        api.get_vacancies(pages_count=2)
        vacancies_json.extend(api.get_formatted_vacancies())

    connector = Connector(keyword=keyword)
    connector.insert(vacancies_json=vacancies_json)
    connector.select(vacancies_json=vacancies_json)
    # vacancy_1 = Vacancy("1234567", "Разработчик", "http/developer", "Headhunter", 100000, 120000, "RUR", 1)
    # vacancy_2 = Vacancy("1234567", "Тестировщик", "http/developer", "SuperJob", 120000, 140000, "RUR", 1)
    # vacancy_1.sorted_by_salary(150000)
    # vacancy_2.sorted_by_salary(150000)

    while True:
        command = input(
            "1 - Вывести список вакансий;\n"
            "2 - Отсортировать по минимальной зарплате;\n"
            "exit - для выхода.\n"
            ">>> "
        )
        if command.lower() == "exit":
            break
        elif command == "1":
            vacancies = connector.select("Python")
        elif command == "2":
            vacancies = vacancy.sorted_by_salary(150000)

        for vacancy in vacancies:
            print(vacancy, end="\n")

if __name__ == "__main__":
    main()
