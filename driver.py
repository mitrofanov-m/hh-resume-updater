from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from contextlib import contextmanager
from time import sleep
from settings import EMAIL


class WebDriver:
    __devices = {
        'desktop': {
            'login_btn': '/html/body/div[5]/div[3]/div/div[1]/div[1]/div/div[5]/a',
            'email_in': '/html/body/div[6]/div/div[1]/div[4]/div/div/div/div/div/div/div[1]/div[1]/div[1]/div[2]/div/div/form/div[1]/input',
            'email_key_in': '//*[@id="HH-React-Root"]/div/div/div/div/div/div/div/div/div/div/div/div/form/div[1]/div/div[1]/input'
        },
        'mobile': None
    }

    def __init__(self, timeout=False):
        # TODO: сделать два агента: телефон и комп и выбор агента рандомно
        print('__init__ method called')
        self.device = self.__devices['desktop']
        self.driver = webdriver.Chrome()
        self.email = EMAIL
        sleep(2)

    def __enter__(self):
        print('__enter__ method called')
        self.login()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.driver.quit()
        if exception_type is not None:
            traceback.print_exception(exception_type, exception_value, traceback)
        
        return True
        

    def login(self):
        self.driver.get('https://hh.ru/')
        login_btn = self.driver.find_element_by_xpath(self.device['login_btn'])
        login_btn.click()
        sleep(12)
        email_in = self.driver.find_element_by_xpath(self.device['email_in'])
        email_in.clear()
        sleep(9)
        email_in.send_keys(self.email)
        sleep(14)
        email_in.send_keys(Keys.RETURN)
        sleep(8)

        # тут ждет кода с почты
        email_key_in = self.driver.find_element_by_xpath(self.device['email_key_in'])
        email_key_in.clear()
        key = input('Email key: ')
        # TODO: validate key \d{4}
        email_key_in.send_keys(key)
        sleep(2)
        email_key_in.send_keys(Keys.RETURN)