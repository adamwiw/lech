from functools import reduce
from json import loads

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from seleniumwire.request import Request
from seleniumwire.utils import decode
from seleniumwire.webdriver import Chrome

from question import Question


def request_filter(request: Request):
    return request.method == 'POST' and \
           request.url.find('https://lech.pl') > -1 and \
           request.url.find('age-verification') == -1


def save_question(previous: Request, current: Request) -> Request:
    body = decode(current.response.body, current.response.headers.get('Content-Encoding', 'identity'))
    response = loads(body)
    response_type = response.get('type')
    data = response.get('data')
    if response_type == 'question_result':
        should_select = data.get('shouldSelect')
        body = decode(previous.response.body, previous.response.headers.get('Content-Encoding', 'identity'))
        response = loads(body)
        response_type = response.get('type')
        property_name = 'nextScreenHtml' if response_type == 'question_result' else 'quizScreenHtml'
        soup = BeautifulSoup(response.get('data').get(property_name), features='html.parser')
        question = soup.find('h2', 'quiz-section__title--question').text.strip()
        answers = list(map(lambda i: i.text, soup.find_all('span', 'quiz__choice-span')))
        labels = soup.find_all('label', 'quiz__choice')
        correct_answer = list(filter(lambda i: i.find('input', {'value': should_select}) is not None, labels))
        answer = correct_answer[0].find('span').text
        if not len(Question.objects(question=question)):
            Question(question=question, answers=answers, answer=answer).save()
    return current


class Lech:
    def __init__(self) -> None:
        self.__chrome = Chrome()
        self.__chrome.maximize_window()

    def __del__(self) -> None:
        self.__chrome.close()

    def accept_cookies(self) -> None:
        self.__chrome.get('https://lech.pl/')
        button = self.__chrome.find_element(By.CLASS_NAME, 'acceptAll')
        button.click()

    def __find_element(self, key: str) -> WebElement:
        return self.__chrome.find_element(By.NAME, f'age_verify[{key}]')

    def age_verification(self, **birthday) -> None:
        elements = {key: self.__find_element(key) for key in birthday.keys()}
        for key in elements:
            elements[key].clear()
            elements[key].send_keys(birthday[key])
        button = self.__chrome.find_element(By.NAME, 'age_verify[enter]')
        button.click()

    def play(self) -> None:
        button = self.__chrome.find_element(By.ID, 'btn__main-quiz-start')
        button.click()
        button = self.__chrome.find_element(By.CSS_SELECTOR, 'a[data-txt="Graj"]')
        button.click()

    def save_questions(self):
        requests = list(filter(request_filter, self.__chrome.requests))
        reduce(save_question, requests)

    def restart(self):
        button = self.__chrome.find_element(By.CLASS_NAME, 'btn-start-quiz-in-warmup')
        button.click()
        button = self.__chrome.find_element(By.CSS_SELECTOR, 'a[data-txt="Graj"]')
        button.click()
