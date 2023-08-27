from abc import abstractmethod, ABC
from exceptions import ParsingError

import requests
import json
import os

value = os.getenv('X-Api-App-Id')

class Engine(ABC):
    """Абстрактный родительский класс"""

    @abstractmethod
    def get_request(self):
        pass

    @abstractmethod
    def get_vacancies(self):
        pass


class HeadHunterAPI(Engine):
    """Дочерний класс Engine для HeadHunterAPI"""

    url = "https://api.hh.ru/vacancies/"

    def __init__(self, keyword):

        self.params = {
            "per_page": 100,
            "page": int,
            "text": keyword,
            "archived": False,
        }
        self.vacancies = []

    def get_request(self):
        response = requests.get(self.url, params=self.params)
        if response.status_code != 200:
            raise ParsingError(f"Ошибка получения вакансий! Статус: {response.status_code}")
        return response.json()

    def get_formatted_vacancies(self):
        formatted_vacancies = []
        for vacancy in self.vacancies:
            formatted_vacancy = {
                "employer": vacancy["id"],
                "title": vacancy["name"],
                "url": vacancy["url"],
                "api": "HeadHunter",
                "salary_from": vacancy["salary"]["from"] if vacancy["salary"] else None,
                "salary_to": vacancy["salary"]["to"] if vacancy["salary"] else None,
            }
            formatted_vacancies.append(formatted_vacancy)
        return formatted_vacancies

    def get_vacancies(self, pages_count=2):
        self.vacancies = []
        for page in range(pages_count):
            page_vacancies = []
            self.params["page"] = page
            print(f"({self.__class__.__name__}) Парсинг страницы {page} -", end=" ")
            try:
                page_vacancies = self.get_request()
            except ParsingError as error:
                print(error)
            else:
                self.vacancies.extend(page_vacancies["items"])
                print(f"Загружено вакансий: {len(page_vacancies)}")
            if len(page_vacancies) == 0:
                break
        return self.vacancies


class SuperJobAPI(Engine):
    """Дочерний класс Engine для SuperJobAPI"""

    url = "https://api.superjob.ru/2.0/vacancies/"

    def __init__(self, keyword):
        self.params = {
            "count": 100,
            "page": None,
            "keyword": keyword,
            "archive": False,
        }
        self.headers = {
            "X-Api-App-Id": value
        }
        self.vacancies = []

    def get_request(self):
        response = requests.get(self.url, headers=self.headers, params=self.params)
        if response.status_code != 200:
            raise ParsingError(f"Ошибка получения вакансий! Статус: {response.status_code}")
        return response.json()["objects"]

    def get_formatted_vacancies(self):
        formatted_vacancies = []
        for vacancy in self.vacancies:
            formatted_vacancy = {
                "employer": vacancy["firm_name"],
                "title": vacancy["profession"],
                "url": vacancy["link"],
                "api": "SuperJob",
                "salary_from": vacancy["payment_from"] if vacancy["payment_from"] and vacancy[
                    "payment_from"] != 0 else None,
                "salary_to": vacancy["payment_to"] if vacancy["payment_to"] and vacancy["payment_to"] != 0 else None,
            }
            formatted_vacancies.append(formatted_vacancy)

        return formatted_vacancies

    def get_vacancies(self, pages_count=2):
        self.vacancies = []
        for page in range(pages_count):
            page_vacancies = []
            self.params["page"] = page
            print(f"({self.__class__.__name__}) Парсинг страницы {page} -", end=" ")
            try:
                page_vacancies = self.get_request()
            except ParsingError as error:
                print(error)
            else:
                self.vacancies.extend(page_vacancies)
                print(f"Загружено вакансий: {len(page_vacancies)}")
            if len(page_vacancies) == 0:
                break
        return self.vacancies


class Vacancy:

    def __init__(self, employer, title, url, api, salary_from, salary_to):
        self.employer = employer
        self.title = title
        self.url = url
        self.api = api
        self.salary_from = salary_from
        self.salary_to = salary_to

    def __str__(self):
        return f"Работодатель: {self.employer}\n" \
               f"Вакансия: {self.title}\n" \
               f"Зарплата: от {self.salary_from} до {self.salary_to}\n" \
               f"Ссылка: {self.url}"

    def __ge__(self, other):
        if self.salary_from and other.salary_from != None:
            return self.salary_from >= other.salary_from

    def __lt__(self, other):
         if self.salary_from and other.salary_from != None:
            return self.salary_from < other.salary_from


class Connector:

    def __init__(self, keyword):
        self.filename = f"{keyword.title()}.json"

    def insert(self, vacancies_json):
        self.vacancies_json = vacancies_json
        """Записывает информацию в файл"""

        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(self.vacancies_json, file, indent=4, ensure_ascii=False)

    def select(self, vacancies_json):
        self.vacancies_json = vacancies_json
        """Открывает для чтения информацию из файла"""

        with open(self.filename, "r", encoding="utf-8") as file:
            vacancies = json.load(file)
        return [Vacancy(**x) for x in vacancies]
    

    def sorted_by_salary(self):
        self.vacancies = []

        with open("Python.json", "r", encoding="utf-8") as file:
            vacancies = json.load(file)
        self.vacancies = [Vacancy(**x) for x in vacancies]
        self.vacancies.sort()
        return self.vacancies
