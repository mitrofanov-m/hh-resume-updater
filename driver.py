from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from contextlib import contextmanager
from time import sleep
import traceback
from settings import EMAIL


class WebDriver:
    __xpaths_of = {
        'desktop':{
            'login_btn': "(//a[text() = 'Войти']/parent::div[contains(@class, 'item_no-mobile')]/child::a)[2]",
            'email_in': "(//input[@placeholder='Email или телефон' or @name='login'])",
            'email_key_in': "(//input[@placeholder='Введите код' or @name='otp-code-input'])",
            'my_resume': "(//a[text()='Мои резюме' or @data-qa='mainmenu_myResumes'])"
        },
        'desktop_absolute': {
            'login_btn': '/html/body/div[5]/div[3]/div/div[1]/div[1]/div/div[5]/a',
            'email_in': '/html/body/div[6]/div/div[1]/div[4]/div/div/div/div/div/div/div[1]/div[1]/div[1]/div[2]/div/div/form/div[1]/input',
            'email_key_in': '//*[@id="HH-React-Root"]/div/div/div/div/div/div/div/div/div/div/div/div/form/div[1]/div/div[1]/input',
            'my_resume': "//a[text()='Мои резюме']"
        },
        'mobile': {
            'login_btn': "(//a[text()='Войти' ]/parent::div[contains(@class, 'item_mobile')]/child::a)[1]",
            'email_in': "(//input[@placeholder='Email или телефон' or @name='login'])",
            'email_key_in': "(//input[@placeholder='Введите код' or @name='otp-code-input'])"
        }
    }

    def __init__(self, timeout=False):
        # TODO: сделать два агента: телефон и комп и выбор агента рандомно
        print('__init__ method called')
        self.xpath = self.__xpaths_of['desktop']
        self.driver = webdriver.Chrome()
        self.email = EMAIL
        sleep(2)

    def __enter__(self):
        print('__enter__ method called')
        self.login()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.quit()
        if exception_type is not None:
            traceback.print_exception(value=exception_value, tb=traceback)
        
        return True
        

    def login(self):
        self.driver.get('https://hh.ru/')
        login_btn = self.driver.find_element_by_xpath(self.xpath['login_btn'])
        login_btn.click()
        sleep(12)
        email_in = self.driver.find_element_by_xpath(self.xpath['email_in'])
        email_in.clear()
        sleep(9)
        email_in.send_keys(self.email)
        sleep(14)
        email_in.send_keys(Keys.RETURN)
        sleep(8)

        # тут ждет кода с почты
        email_key_in = self.driver.find_element_by_xpath(self.xpath['email_key_in'])
        email_key_in.clear()
        key = input('Email key: ')
        # TODO: validate key \d{4}
        email_key_in.send_keys(key)
        sleep(2)
        email_key_in.send_keys(Keys.RETURN)

    def quit(self):
        self.driver.quit()


if __name__ == '__main__':
    with WebDriver() as bot:
        print("logined quite")