from classes import HeadHunterAPI, SuperJobAPI, Vacancy, Connector


def main():
    vacancies_json = []
    keyword = "Python"

    """Создание экземпляров класса для работы с API сайтов с вакансиями"""
    hh = HeadHunterAPI(keyword)
    sj = SuperJobAPI(keyword)

    """Получение вакансий с разных платформ"""
   
    for api in (hh, sj):
        api.get_vacancies(pages_count=2)
        vacancies_json.extend(api.get_formatted_vacancies())

    connector = Connector(keyword=keyword)
    connector.insert(vacancies_json=vacancies_json)
    connector.select(vacancies_json=vacancies_json)
    vacancy = Vacancy("1234567", "Разработчик", "http/developer", "Headhunter", 100000, 120000)
    #vacancy.sorted_by_salary()


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
            vacancies = connector.sorted_by_salary()
        for vacancy in vacancies:
            print(vacancy, end="\n")


if __name__ == "__main__":
    main()
