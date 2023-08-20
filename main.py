import requests
from classes import HeadHunterAPI, SuperJobAPI, Vacancy, Connector
from utils import get_currencies

# Сохранение информации о вакансиях в файл
# json_saver = JSONSaver()
# json_saver.add_vacancy(vacancy)
# json_saver.get_vacancies_by_salary("100 000-150 000 руб.")
# json_saver.delete_vacancy(vacancy)


def main():
    vacancies_json = []
    keyword = "Python"

    """Создание экземпляров класса для работы с API сайтов с вакансиями"""
    hh = HeadHunterAPI(keyword)
    sj = SuperJobAPI(keyword)

    """Получение вакансий с разных платформ"""
    hh_vacancies = hh.get_vacancies()
    print(hh_vacancies)
    sj_vacancies = sj.get_vacancies()
    print(sj_vacancies)

    for api in (hh, sj):
        api.get_vacancies(pages_count=2)
        vacancies_json.extend(api.get_formatted_vacancies())

    connector = Connector(keyword=keyword, vacancies_json=vacancies_json)
    connector.insert(vacancies_json=vacancies_json)

    """Создание экземпляра класса для работы с вакансиями"""
    vacancy = Vacancy("Python Developer", "<https://hh.ru/vacancy/123456>", "100 000-150 000 руб.",
                      "Требования: опыт работы от 3 лет...")
    print(vacancy)

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
            vacancies = connector.select()
        elif command == "2":
            vacancies = connector.Vacancy

        for vacancy in vacancies:
            print(vacancy, end="\n")

#Функция для взаимодействия с пользователем
def user_interaction():
    platforms = ["HeadHunter", "SuperJob"]
    search_query = input("Введите поисковый запрос: ")
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    filtered_vacancies = Vacancy(filter_words)

    if not filtered_vacancies:
        print("Нет вакансий, соответствующих заданным критериям.")
        return

    sorted_vacancies = Vacancy(filtered_vacancies)
    top_vacancies = Vacancy(sorted_vacancies, top_n)
    print(top_vacancies)


if __name__ == "__main__":
    main()
    #user_interaction()