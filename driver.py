from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from contextlib import contextmanager
from time import sleep
import traceback
from settings.settings import EMAIL, HH_PASSWORD, HH_RESUME
from selenium.common.exceptions import NoSuchElementException
from hh_mail import *
import pickle


class HeadHunterBot:
    __xpaths_of = {
        'desktop':{
            'login_btn': "(//a[text() = 'Войти']/parent::div[contains(@class, 'item_no-mobile')]/child::a)[2]",
            'email_in': "(//input[@placeholder = 'Email или телефон' or @name = 'login'])",
            'email_key_in': "(//input[@placeholder = 'Введите код' or @name = 'otp-code-input'])",
            'my_resume': "//a[text() = 'Мои резюме' or @data-qa = 'mainmenu_myResumes']",
            'switch_to_pass': "//span[@class = 'bloko-link-switch']",
            'pass_in': "//input[@type = 'password']",
            'login_submit': '//button[@class = "bloko-button bloko-button_primary"]',
            'profile_btn': "//button[contains(@data-qa,'applicantProfile')]",
            'update_btn': f"//div[@data-qa = 'resume' and @data-qa-title = '{HH_RESUME}']" \
                           "//descendant::div[@class = 'applicant-resumes-recommendations-button']" \
                           "//child::button[@data-qa = 'resume-update-button']"
        },
        'mobile': {
            'login_btn': "(//a[text() = 'Войти']/parent::div[contains(@class, 'item_mobile')]/child::a)[1]",
            'email_in': "(//input[@placeholder = 'Email или телефон' or @name = 'login'])",
            'email_key_in': "(//input[@placeholder = 'Введите код' or @name = 'otp-code-input'])",
            'mainmenu_mobile_btn': "//button[@data-qa = 'mainmenu_mobile']",
            'my_resume': "//a[text() = 'Мои резюме' and contains(@data-qa, 'xs')]",
            'update_btn': f"//div[@data-qa = 'resume' and @data-qa-title = '{HH_RESUME}']" \
                           "//descendant::div[@class='applicant-resumes-recommendations-button']" \
                           "//child::button[@data-qa='resume-update-button']"

        }
    }


    def __init__(self,device='desktop', invisible=False):
        print('__init__ method called')
        self.xpath = self.__xpaths_of[device]
        self.driver = None
        self.email = EMAIL
        self.password = HH_PASSWORD
        self.options = None
        
        if invisible:
            self.options = webdriver.ChromeOptions()
            self.options.headless = True


    def __enter__(self):
        print('__enter__ method called')
        self.enter()
        return self


    def __exit__(self, exception_type, exception_value, traceback):
        self.quit()
        #if exception_type is not None:
        #    traceback.print_exception(value=exception_value, tb=traceback)
        return True


    @property
    def authorized(self):
        try:
            self.driver.find_element_by_xpath(self.xpath['profile_btn'])
            return True
        except NoSuchElementException:
            return False


    def click_on(self, btn):
        sleep(7)
        login_btn = self.driver.find_element_by_xpath(self.xpath[btn])
        login_btn.click()


    def write_to(self, input_field, data):
        sleep(9)
        field_in = self.driver.find_element_by_xpath(self.xpath[input_field])
        field_in.clear()
        sleep(5)
        for i in data:
            field_in.send_keys(i)
            sleep(0.5)
        return field_in

    def _update_cookies(self)-> bool:
        sleep(8)
        if self.authorized:
            pickle.dump(self.driver.get_cookies(), open('settings/cookies.pkl', "wb"))
            print('Cookies have been updated.')
            return True
        return False
        

    def _set_cookies(self)-> bool:
        try:
            cookies = pickle.load(open('settings/cookies.pkl', "rb"))
        except FileNotFoundError:
            return False

        for cookie in cookies:
                if 'expiry' in cookie:
                    del cookie['expiry']
                self.driver.add_cookie(cookie)
        sleep(5)
        self.driver.refresh()
        
        return self.authorized


    def start(self):
        self.driver.get('https://hh.ru/')
        if not self._set_cookies():
            self.login()


    def login(self)-> bool:
        self.click_on('login_btn')
        email_in = self.write_to('email_in', self.email)
        sleep(11)
        email_in.send_keys(Keys.RETURN)
        sleep(30)
        key = get_email_key()
        if key is None:
            raise ValueError('Incorrect email key') 
        email_key_in = self.write_to('email_key_in', key)
        sleep(11)
        email_key_in.send_keys(Keys.RETURN)
        return self._update_cookies()


    def enter(self):
        if not self.options:
            self.driver = webdriver.Chrome()
        else:
            self.driver = webdriver.Chrome(options=self.options)



    def quit(self):
        self.driver.close()
        self.driver.quit()


def push_higher_in_search():
    with HeadHunterBot(invisible=True) as bot:
        bot.start()
        print("logined quite")
        bot.click_on('my_resume')
        try:
            bot.click_on('update_btn')
        except NoSuchElementException:
            print('Cannot update now, try again later.')
        sleep(10)


if __name__ == '__main__':
    push_higher_in_search()