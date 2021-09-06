from hhbot.driver import HeadHunterBot
from time import sleep
from settings.settings import EMAIL, HH_PASSWORD, HH_RESUME, email_settings


def push_higher_in_search():
    with HeadHunterBot(EMAIL, HH_PASSWORD, HH_RESUME, email_settings, invisible=False) as bot:
        bot.start()
        print("logined quite")
        bot.update_resume()
        sleep(10)


if __name__ == '__main__':
    push_higher_in_search()