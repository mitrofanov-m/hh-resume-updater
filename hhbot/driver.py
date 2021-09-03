from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import pickle
from .mailparser import *


class HeadHunterBot:
    def __init__(self,HH_EMAIL, HH_PASSWORD, HH_RESUME, email_settings, device='desktop', invisible=False):
        self.email = HH_EMAIL
        self.password = HH_PASSWORD
        self.resume = HH_RESUME
        self.email_settings = email_settings
        self.xpath = self.__xpaths_of[device]
        self.driver = None
        
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
        return True

    @property
    def __xpaths_of(self):
        return {
        'desktop':{
            'login_btn': "(//a[text() = 'Войти']/parent::div[contains(@class, 'item_no-mobile')]/child::a)[2]",
            'email_in': "(//input[@placeholder = 'Email или телефон' or @name = 'login'])",
            'email_key_in': "(//input[@placeholder = 'Введите код' or @name = 'otp-code-input'])",
            'my_resume': "//a[text() = 'Мои резюме' or @data-qa = 'mainmenu_myResumes']",
            'switch_to_pass': "//span[@class = 'bloko-link-switch']",
            'pass_in': "//input[@type = 'password']",
            'login_submit': '//button[@class = "bloko-button bloko-button_primary"]',
            'profile_btn': "//button[contains(@data-qa,'applicantProfile')]",
            'update_btn': f"//div[@data-qa = 'resume' and @data-qa-title = '{self.resume}']" \
                           "//descendant::div[@class = 'applicant-resumes-recommendations-button']" \
                           "//child::button[@data-qa = 'resume-update-button']",
            'history_btn': f"//div[@data-qa = 'resume' and @data-qa-title = '{self.resume}']" \
                           "//descendant::a[contains(@href, 'resumeview/history')]"
        },
        'mobile': {
            'login_btn': "(//a[text() = 'Войти']/parent::div[contains(@class, 'item_mobile')]/child::a)[1]",
            'email_in': "(//input[@placeholder = 'Email или телефон' or @name = 'login'])",
            'email_key_in': "(//input[@placeholder = 'Введите код' or @name = 'otp-code-input'])",
            'mainmenu_mobile_btn': "//button[@data-qa = 'mainmenu_mobile']",
            'my_resume': "//a[text() = 'Мои резюме' and contains(@data-qa, 'xs')]",
            'update_btn': f"//div[@data-qa = 'resume' and @data-qa-title = '{self.resume}']" \
                           "//descendant::div[@class='applicant-resumes-recommendations-button']" \
                           "//child::button[@data-qa='resume-update-button']",
                           
            'history_btn': f"//div[@data-qa = 'resume' and @data-qa-title = '{self.resume}']" \
                           "//descendant::a[contains(@href, 'resumeview/history')]"

        }
    }

    @property
    def authorized(self):
        try:
            self.find_element('profile_btn')
            print('authorized')
            return True
        except Exception as e:
            print(e)
            print('not authorized')
            return False


    def find_element(self, key) -> WebElement:
        if key in self.xpath.keys():
            element = self.driver.find_element_by_xpath(self.xpath[key])
        else:
            element = self.driver.find_element_by_xpath(key)
        return element

    
    def find_elements(self, key) -> list:
        if key in self.xpath.keys():
            elements = self.driver.find_elements_by_xpath(self.xpath[key])
        else:
            elements = self.driver.find_elements_by_xpath(key)
        return elements


    def click_on(self, btn):
        sleep(7)
        btn_element = self.find_element(btn)
        btn_element.click()


    def write_to(self, input_field, data) -> WebElement:
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

    def _update_cookies(self) -> bool:
        sleep(8)
        if self.authorized:
            pickle.dump(self.driver.get_cookies(), open('settings/cookies.pkl', "wb"))
            print('Cookies have been updated.')
            return True
        return False
        

    def _set_cookies(self) -> bool:
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
        print('_set_cookies: refreshed')
        return self.authorized


    def start(self) -> bool:
        self.driver.get('https://hh.ru/')
        recovered = self._set_cookies()
        print('cookies seted')
        if not recovered:
            self.login()
            print('logined')
            self._update_cookies()
            print('cookies updated')
        return recovered


    def login(self) -> bool:
        self.click_on('login_btn')
        email_in = self.write_to('email_in', self.email)
        sleep(11)
        email_in.send_keys(Keys.RETURN)
        sleep(30)
        key = get_email_key(self.email_settings)
        if key is None:
            print('Incorrect email key')
            raise ValueError
        email_key_in = self.write_to('email_key_in', key)
        sleep(11)
        email_key_in.send_keys(Keys.RETURN)
        return True

    
    def update_resume(self) -> bool:
        sleep(10)
        self.click_on('my_resume')
        try:
            self.click_on('update_btn')
        except NoSuchElementException:
            print('Cannot update now, try again later.')
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
