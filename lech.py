from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


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
