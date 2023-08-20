from abc import abstractmethod, ABC
from exceptions import ParsingError

import requests
import json
import os

#value = os.getenv('API_KEY')


class Engine(ABC):
    """Абстрактный родительский класс"""
    @abstractmethod
    def get_request(self):
        """Получаем информацию с сайта"""

        pass

    @abstractmethod
    def get_vacancies(self):
        """Получаем вакансии"""

        pass

class HeadHunterAPI(Engine):
    """Дочерний класс Engine для HeadHunterAPI"""

    url = "https://api.hh.ru/vacancies/"

    def __init__(self, keyword):
        self.vacancies = []
        self.params = {
            "per_page": 100,
            "page": None,
            "text": keyword,
            "archive": False,
        }

    def get_request(self):
        response = requests.get(self.url, params=self.params)
        if response.status_code != 200:
            raise ParsingError(f"Ошибка получения вакансий! Статус: {response.status_code}")
        return response.json() #["objects"]

    def get_formatted_vacancies(self):
        formatted_vacancies = []
        #currencies = get_currencies()
        sj_currencies = {
            "rub": "RUR",
            "uah": "UAH",
            "uzs": "UZS",
        }

        for vacancy in self.vacancies:
            formatted_vacancy = {
                "employer": vacancy["firm_name"],
                "title": vacancy["profession"],
                "url": vacancy["link"],
                "api": "SuperJob",
                "salary_from": vacancy["payment_from"] if vacancy["payment_from"] and vacancy["payment_from"] != 0 else None,
                "salary_to": vacancy["salary_to"] if vacancy["salary_to"] and vacancy["salary_to"] != 0 else None,
            }
            if vacancy["currency"] in sj_currencies:
                formatted_vacancy["currency"] = sj_currencies[vacancy["currency"]]
                formatted_vacancy["currency_value"] = sj_currencies[sj_currencies[vacancy["currency"]]] in sj_currencies[vacancy["currency"]]
            elif vacancy["currency"]:
                formatted_vacancy["currency"] = "RUR"
                formatted_vacancy["currency_value"] = 1
            else:
                formatted_vacancy["currency"] = None
                formatted_vacancy["currency_value"] = None

            formatted_vacancies.append(formatted_vacancy)

        return formatted_vacancies


    def get_vacancies(self, pages_count: int=2):
        self.__class__.name__ = None
        for page in range(pages_count):
            page_vacancies = []
            self.params["page"] = page
            print(f"({self.__class__.name__}) Парсинг страницы { page } -", end=" ")
            try:
                page_vacancies = self.get_request()
            except ParsingError as error:
                print(error)
            else:
                self.vacancies.extend(page_vacancies)
                print(f"Загружено вакансий: { len(page_vacancies) }")
            if len(page_vacancies) == 0:
                break


class SuperJobAPI(Engine):
    """Дочерний класс Engine для SuperJobAPI"""

    url = "https://api.superjob.ru/2.0/vacancies/"

    def init(self, keyword):
        self.params = {
            "count": 100,
            "page": None,
            "keyword": keyword,
            "archive": False,
        }
        self.headers = {
            "X-Api-App-Id": "v3.r.137756487.adf52d67576949fc227e9a44484f486d9ae8183c.c85c473c1a3d7451e8549432293d922bdcf27e12"
        }
        self.vacancies = []

    def get_request(self):
        response = requests.get(self.url, headers=self.headers, params=self.params)
        if response.status_code != 200:
            raise ParsingError(f"Ошибка получения вакансий! Статус: {response.status_code}")
        return response.json()["objects"]

    def get_formatted_vacancies(self):
        formatted_vacancies = []
        #currencies = get_currencies()
        sj_currencies = {
            "rub": "RUR",
            "uah": "UAH",
            "uzs": "UZS",
        }

        for vacancy in self.vacancies:
            formatted_vacancy = {
                "employer": vacancy["firm_name"],
                "title": vacancy["profession"],
                "url": vacancy["link"],
                "api": "SuperJob",
                "salary_from": vacancy["payment_from"] if vacancy["payment_from"] and vacancy["payment_from"] != 0 else None,
                "salary_to": vacancy["salary_to"] if vacancy["salary_to"] and vacancy["salary_to"] != 0 else None,
            }
            if vacancy["currency"] in sj_currencies:
                formatted_vacancy["currency"] = sj_currencies[vacancy["currency"]]
                formatted_vacancy["currency_value"] = sj_currencies[sj_currencies[vacancy["currency"]]] in sj_currencies[vacancy["currency"]]
            elif vacancy["currency"]:
                formatted_vacancy["currency"] = "RUR"
                formatted_vacancy["currency_value"] = 1
            else:
                formatted_vacancy["currency"] = None
                formatted_vacancy["currency_value"] = None

            formatted_vacancies.append(formatted_vacancy)

        return formatted_vacancies


    def get_vacancies(self, pages_count=2):
        self.vacanсies = []
        for page in range(pages_count):
            page_vacancies = []
            self.params["page"] = page
            print(f"({self.__class__.name__}) Парсинг страницы { page } -", end=" ")
            try:
                page_vacancies = self.get_request()
            except ParsingError as error:
                print(error)
            else:
                self.vacanсies.extend(page_vacancies)
                print(f"Загружено вакансий: { len(page_vacancies) }")
            if len(page_vacancies) == 0:
                break

class Vacancy:

    def __init__(self, vacancy):
        self.employer = vacancy["employer"]
        self.title = vacancy["title"]
        self.url = vacancy["url"]
        self.api = vacancy["api"]
        self.salary_from = vacancy["salary_from"]
        self.salary_to = vacancy["salary_to"]
        self.currency = vacancy["currency"]
        self.currency_value = vacancy["currency_value"]

    def __str__(self):
        if not self.salary_from and not self.salary_to:
            salary = "Не указана"
        else:
            salary_from, salary_to = "", ""
            if self.salary_from:
                salary_from = f" от { self.salary_from } { self.currency }"
                if self.currency != "RUR":
                    salary_from += f"({ round(self.salary_from * self.currency_value, 2) } RUR)"
            if self.salary_to:
                salary_to = f" до {self.salary_to} {self.currency}"
                if self.currency != "RUR":
                    salary_to += f"({round(self.salary_to * self.currency_value, 2)} RUR)"
            salary = " ".join([salary_from, salary_to]).strip()
        return f"""
Работодатель: \"{ self.employer }\"
Вакансия: \"{ self.title }\"
Зарплата: { salary }
Ссылка: { self.url }
        """
    def __le__(self, other):
        pass

    def __ge__(self, other):
        pass

class Connector:

    def __init__(self, keyword, vacancies_json):
        self.filename = f"{ keyword.title() }.json"
        #self.insert(vacancies_json)

    def insert(self, vacancies_json):
        """Записывает информацию в файл"""

        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(vacancies_json, file, indent=4, ensure_ascii=False)

    def select(self):
        """Открывает для чтения информацию из файла"""

        with open(self.filename, "r", encoding="utf-8") as file:
            vacancies = json.load(file)
        return [Vacancy(x) for x in vacancies]