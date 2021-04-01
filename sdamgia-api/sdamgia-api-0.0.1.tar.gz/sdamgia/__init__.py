# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests


class sdamgia:
    def __init__(self):
        self._BASE_DOMAIN = 'sdamgia.ru'
        self._SUBJECT_BASE_URL = {
            'math': f'https://math-ege.{self._BASE_DOMAIN}', 'mathb': f'https://mathb-ege.{self._BASE_DOMAIN}',
            'phys': f'https://phys-ege.{self._BASE_DOMAIN}',
            'inf': f'https://inf-ege.{self._BASE_DOMAIN}',
            'rus': f'https://rus-ege.{self._BASE_DOMAIN}',
            'bio': f'https://bio-ege.{self._BASE_DOMAIN}',
            'en': f'https://en-ege.{self._BASE_DOMAIN}',
            'chem': f'https://chem-ege.{self._BASE_DOMAIN}',
            'geo': f'https://geo-ege.{self._BASE_DOMAIN}',
            'soc': f'https://soc-ege.{self._BASE_DOMAIN}',
            'de': f'https://de-ege.{self._BASE_DOMAIN}',
            'fr': f'https://fr-ege.{self._BASE_DOMAIN}',
            'lit': f'https://lit-ege.{self._BASE_DOMAIN}',
            'sp': f'https://sp-ege.{self._BASE_DOMAIN}',
            'hist': f'https://hist-ege.{self._BASE_DOMAIN}',
        }

    def get_problem_by_id(self, subject, id):
        """
        Получение информации о задаче по ее идентификатору
        :pararepm subject: Наименование предмета, строка
        :param id: Идентификатор задачи, строка
        :return: Словарь, хранящий id задачи, тему, условие и решение задачи (содержат как сам текст, так и вложения
         в виде списка ссылок на svg изображения), ответ, список аналогов и ссылка на задачу на sdamgia
        """

        doujin_page = requests.get(f'{self._SUBJECT_BASE_URL[subject]}/problem?id={id}')
        soup = BeautifulSoup(doujin_page.content, 'html.parser')

        probBlock = soup.find('div', {'class': 'prob_maindiv'})
        if probBlock is None:
            return None

        URL = f'{self._SUBJECT_BASE_URL[subject]}/problem?id={id}'
        TOPIC_ID = ' '.join(probBlock.find('span', {'class': 'prob_nums'}).text.split()[1:][:-2])
        ID = id

        CONDITION, SOLUTION, ANSWER, ANALOGS = {}, {}, '', []

        if probBlock.find_all('div', {'class': 'pbody'})[0]:
            CONDITION = {'text': probBlock.find_all('div', {'class': 'pbody'})[0].text,
                         'images': [i['src'] for i in probBlock.find_all('div', {'class': 'pbody'})[0].find_all('img')]
                         }
        if probBlock.find_all('div', {'class': 'pbody'})[1]:
            SOLUTION = {'text': probBlock.find_all('div', {'class': 'pbody'})[1].text,
                        'images': [i['src'] for i in probBlock.find_all('div', {'class': 'pbody'})[1].find_all('img')]
                        }
        if probBlock.find('div', {'class': 'answer'}):
            ANSWER = probBlock.find('div', {'class': 'answer'}).text.replace('Ответ: ', '')
        if probBlock.find('div', {'class': 'minor'}).find_all('a'):
            ANALOGS = [i.text for i in probBlock.find('div', {'class': 'minor'}).find_all('a')]
            if 'Все' in ANALOGS: ANALOGS.remove('Все')


        return {'id': ID, 'topic': TOPIC_ID, 'condition': CONDITION, 'solution': SOLUTION, 'answer': ANSWER,
                'analogs': ANALOGS, 'url': URL}

    def search(self, subject, request, page=1):
        """
        Поиск задач по запросу
        :param subject: Наименование предмета, строка
        :param request: Запрос, строка
        :param page: Номер страницы поиска, целое число
        :return: Список идентификаторов найденных задач
        """
        doujin_page = requests.get(f'{self._SUBJECT_BASE_URL[subject]}/search?search={request}&page={str(page)}')
        soup = BeautifulSoup(doujin_page.content, 'html.parser')
        return [i.text.split()[-1] for i in soup.find_all('span', {'class': 'prob_nums'})]

    def get_test_by_testid(self, subject, testid):
        """
        :param subject: Наименование предмета, строка
        :param testid: Идентификатор теста, строка
        :return: Список идентификаторов задач, включенных в тест
        """
        doujin_page = requests.get(f'{self._SUBJECT_BASE_URL[subject]}/test?id={testid}')
        soup = BeautifulSoup(doujin_page.content, 'html.parser')
        return [i.text.split()[-1] for i in soup.find_all('span', {'class': 'prob_nums'})]

    def get_catalog(self, subject):
        """
        :param subject: Наименование предмета, строка
        :return: Возвращает каталог задач предмета
        """

        doujin_page = requests.get(f'{self._SUBJECT_BASE_URL[subject]}/prob_catalog')
        soup = BeautifulSoup(doujin_page.content, 'html.parser')
        catalog = []
        CATALOG = []

        for i in soup.find_all('div', {'class': 'cat_category'}):
            try:
                i['data-id']
            except:
                catalog.append(i)

        for topic in catalog[1:]:
            TOPIC_NAME = topic.find('b', {'class': 'cat_name'}).text.split('. ')[1]
            TOPIC_ID = topic.find('b', {'class': 'cat_name'}).text.split('. ')[0]
            if TOPIC_ID[0] == ' ': TOPIC_ID = TOPIC_ID[2:]
            if TOPIC_ID.find('Задания ') == 0: TOPIC_ID = TOPIC_ID.replace('Задания ', '')

            CATALOG.append(
                dict(
                    topic_id=TOPIC_ID,
                    topic_name=TOPIC_NAME,
                    categories=[
                        dict(
                            category_id=i['data-id'],
                            category_name=i.find('a', {'class':'cat_name'}).text
                        )
                        for i in topic.find('div', {'class': 'cat_children'}).find_all('div', {'class': 'cat_category'})]
                )
            )

        return CATALOG


if __name__ == '__main__':
    sdamgia = sdamgia()

