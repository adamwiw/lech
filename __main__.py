from selenium import webdriver


class Lech:
    def __init__(self):
        self.__driver = webdriver.Chrome()
    
    def __del__(self):
        self.__driver.close()

if __name__ == "__main__":
    Lech()
