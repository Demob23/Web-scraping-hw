# Попробуем получать интересующие вакансии на сайте headhunter самыми первыми :)
#
# Необходимо парсить страницу со свежими вакансиями с поиском по "Python" и городами "Москва" и "Санкт-Петербург".
# Эти параметры задаются по ссылке
# Нужно выбрать те вакансии, у которых в описании есть ключевые слова "Django" и "Flask".
# Записать в json информацию о каждой вакансии - ссылка, вилка зп, название компании, город.
import random
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import json
import lxml

vacancies = []
vacancies_urls = []
with webdriver.Firefox() as driver:

    driver.get(f"https://spb.hh.ru/search/vacancy?text=python&area=1&area=2")
    time.sleep(random.randint(2, 8))
    soup = BeautifulSoup(driver.page_source, 'lxml')
    object_urls = soup.find_all(attrs={'class': 'serp-item__title'})
    for ob in object_urls:
        vacancies_urls.append(ob['href'])
    for url in vacancies_urls:
        print(url)
        driver.get(url)
        time.sleep(random.randint(3, 7))
        soup = BeautifulSoup(driver.page_source, 'lxml')
        description = soup.find(class_='vacancy-section').text
        if "django" in description.lower() or 'flask' in description.lower():
            vacancy = {}
            vacancy_name = soup.find(attrs={'class': 'vacancy-title'}).text
            if soup.find('span', attrs={'data-qa': 'vacancy-salary-compensation-type-net'}):
                vacancy_salary = soup.find('span', attrs={'data-qa': 'vacancy-salary-compensation-type-net'}).text
            else:
                vacancy_salary = "Не указана"
            vacancy_company_name = soup.find('a', attrs={'data-qa': 'vacancy-company-name'}).text
            if soup.find(attrs={'data-qa': 'vacancy-view-location'}):
                vacancy_city = soup.find(attrs={'data-qa': 'vacancy-view-location'}).text
            else:
                vacancy_city = soup.find(attrs={'data-qa': 'vacancy-view-raw-address'}).text
            vacancy['name'] = vacancy_name
            vacancy['company'] = vacancy_company_name
            vacancy['city'] = vacancy_city
            vacancy['salary'] = vacancy_salary
            vacancy['url'] = url.strip()
            vacancies.append(vacancy)

with open('vacancies.json', mode='a', encoding='utf-8') as f:
    json.dump(vacancies, f, ensure_ascii=False, indent=4)

