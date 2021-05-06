from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from contextlib import contextmanager
from time import sleep
import traceback
from settings.settings import EMAIL, HH_PASSWORD
from hh_mail import *


class WebDriver:
    __xpaths_of = {
        'desktop':{
            'login_btn': "(//a[text() = 'Войти']/parent::div[contains(@class, 'item_no-mobile')]/child::a)[2]",
            'email_in': "(//input[@placeholder='Email или телефон' or @name='login'])",
            'email_key_in': "(//input[@placeholder='Введите код' or @name='otp-code-input'])",
            'my_resume': "(//a[text()='Мои резюме' or @data-qa='mainmenu_myResumes'])",
            'switch_to_pass': "//span[@class = 'bloko-link-switch']",
            'pass_in': "//input[@type = 'password']",
            'login_submit': '//button[@class="bloko-button bloko-button_primary"]'
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


    def __init__(self,device='desktop', timeout=False):
        print('__init__ method called')
        self.xpath = self.__xpaths_of[device]
        self.driver = None
        self.email = EMAIL
        self.password = HH_PASSWORD
        sleep(2)


    def __enter__(self):
        print('__enter__ method called')
        self.enter()
        return self


    def __exit__(self, exception_type, exception_value, traceback):
        self.quit()
        if exception_type is not None:
            traceback.print_exception(value=exception_value, tb=traceback)
        
        return True


    def _click_on(self, btn):
        sleep(12)
        login_btn = self.driver.find_element_by_xpath(self.xpath[btn])
        login_btn.click()


    def _write_to(self, input_field, data):
        sleep(9)
        field_in = self.driver.find_element_by_xpath(self.xpath[input_field])
        field_in.clear()
        sleep(9)
        for i in data:
            field_in.send_keys(i)
            sleep(0.5)
        return field_in


    def start(self):
        self.driver.get('https://hh.ru/')


    def login(self):
        self._click_on('login_btn')
        email_in = self._write_to('email_in', self.email)
        sleep(11)
        email_in.send_keys(Keys.RETURN)
        sleep(30)
        key = get_email_key()
        if key is None:
            raise ValueError('Incorrect email key') 
        email_key_in = self._write_to('email_key_in', key)
        sleep(11)
        email_key_in.send_keys(Keys.RETURN)


    def enter(self):
        self.driver = webdriver.Chrome()


    def quit(self):
        self.driver.close()
        self.driver.quit()


if __name__ == '__main__':
    with WebDriver() as bot:
        bot.start()
        bot.login()
        sleep(10)
        print("logined quite")