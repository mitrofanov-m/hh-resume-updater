from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement

from contextlib import contextmanager
from time import sleep
import traceback
from settings.settings import EMAIL, HH_PASSWORD, HH_RESUME
from selenium.common.exceptions import NoSuchElementException
from mailparser import *
import pickle
import logging


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
                           "//child::button[@data-qa = 'resume-update-button']",
            'history_btn': f"//div[@data-qa = 'resume' and @data-qa-title = '{HH_RESUME}']" \
                           "//descendant::a[contains(@href, 'resumeview/history')]"
        },
        'mobile': {
            'login_btn': "(//a[text() = 'Войти']/parent::div[contains(@class, 'item_mobile')]/child::a)[1]",
            'email_in': "(//input[@placeholder = 'Email или телефон' or @name = 'login'])",
            'email_key_in': "(//input[@placeholder = 'Введите код' or @name = 'otp-code-input'])",
            'mainmenu_mobile_btn': "//button[@data-qa = 'mainmenu_mobile']",
            'my_resume': "//a[text() = 'Мои резюме' and contains(@data-qa, 'xs')]",
            'update_btn': f"//div[@data-qa = 'resume' and @data-qa-title = '{HH_RESUME}']" \
                           "//descendant::div[@class='applicant-resumes-recommendations-button']" \
                           "//child::button[@data-qa='resume-update-button']",
                           
            'history_btn': f"//div[@data-qa = 'resume' and @data-qa-title = '{HH_RESUME}']" \
                           "//descendant::a[contains(@href, 'resumeview/history')]"

        }
    }


    def __init__(self,device='desktop', invisible=False):
        self.xpath = self.__xpaths_of[device]
        self.driver = None
        self.email = EMAIL
        self.password = HH_PASSWORD
        self.options = None
        
        if invisible:
            self.options = webdriver.ChromeOptions()
            self.options.headless = True


    def __enter__(self):
        logging.info('__enter__ method called')
        self.enter()
        return self


    def __exit__(self, exception_type, exception_value, traceback):
        self.quit()
        return True


    @property
    def authorized(self):
        try:
            self.find_element('profile_btn')
            return True
        except NoSuchElementException:
            return False


    def find_element(self, key)-> WebElement:
        if key in self.xpath.keys():
            element = self.driver.find_element_by_xpath(self.xpath[key])
        else:
            element = self.driver.find_element_by_xpath(key)
        return element

    
    def find_elements(self, key)-> list:
        if key in self.xpath.keys():
            elements = self.driver.find_elements_by_xpath(self.xpath[key])
        else:
            elements = self.driver.find_elements_by_xpath(key)
        return elements


    def click_on(self, btn):
        sleep(7)
        btn_element = self.find_element(btn)
        btn_element.click()


    def write_to(self, input_field, data)-> WebElement:
        sleep(9)
        field_in = self.find_element(input_field)
        # поставить другую очистку
        if field_in.get_attribute("value") != data:
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
            logging.info('Cookies have been updated.')
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


    def start(self)-> bool:
        self.driver.get('https://hh.ru/')
        recovered = self._set_cookies()
        if not recovered:
            self.login()
            self._update_cookies()
        return recovered


    def login(self)-> bool:
        self.click_on('login_btn')
        email_in = self.write_to('email_in', self.email)
        sleep(11)
        email_in.send_keys(Keys.RETURN)
        sleep(30)
        key = get_email_key()
        if key is None:
            logging.error('Incorrect email key')
            raise ValueError
        email_key_in = self.write_to('email_key_in', key)
        sleep(11)
        email_key_in.send_keys(Keys.RETURN)
        return True

    
    def update_resume(self):
        sleep(10)
        self.click_on('my_resume')
        try:
            self.click_on('update_btn')
        except NoSuchElementException:
            logging.info('Cannot update now, try again later.')
            return False
        
        return True


    def enter(self):
        if not self.options:
            self.driver = webdriver.Chrome()
        else:
            self.driver = webdriver.Chrome(options=self.options)


    def quit(self):
        self.driver.close()
        self.driver.quit()


def push_higher_in_search():
    with HeadHunterBot(invisible=False) as bot:
        bot.start()
        logging.info("logined quite")
        bot.update_resume()
        sleep(10)


def parse_views_time():
    with HeadHunterBot(invisible=False) as bot:
        bot.start()
        logging.info("logined quite")
        bot.click_on('my_resume')
        bot.click_on('history_btn')
        sleep(10)
        resume_views = bot.find_elements("//span[@class = 'resume-view-history-views']")
        views_time = []
        for resume_view in resume_views:
            views_time.append(resume_view.text)

        try:
            expandable_btn = bot.find_elements("//span[contains(@class,'bloko-link-switch')]")
            for btn in expandable_btn:
                sleep(7)
                btn.click()
            expandable_views = bot.find_elements("//span[@class='g-expandable']")
            for view in expandable_views:
                view = view.text.split(', ')
                views_time.extend(view)
        except Exception as e:
            logging.warning('no expandable elements')

        return views_time

if __name__ == '__main__':
    push_higher_in_search()