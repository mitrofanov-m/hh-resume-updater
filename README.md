# HeadHunter resume updater
Когда задачу можно решить за 10 минут, но ты нашёл способ автоматизировать решение за 10 дней:
<p align="center">
  <img src="./mem.jpg"  alt="drawing" width="60%"/>
</p>


Сервис hh.ru предоставляет следующую систему заинтересованности соискателя:

>**Как сделать так, чтобы ваше резюме оказалось ближе к топу выдачи, а не к концу?**
>
>*<...> чаще обновляйте ваше резюме — поисковая выдача у работодателей выстраивается в том числе по дате обновления, а значит, после обновления даты ваше резюме поднимается выше. <...>*

Ручное обновление резюме - рутинная задача, а стоимость встроенного функционала автообновления достаточно высока. Данный репозиторий демонстрирует пример создания python библиотеки для автоматизации процесса обновления резюме.


## Installation

Первым делом следует установить актуальную версию браузера chrome. [(click)](https://www.google.com/chrome/)

Затем, установите соответствующий драйвер. Он потребуется для взаимодействия selenium с браузером. [(click)](https://chromedriver.chromium.org/downloads)


Все описанные выше действия, для простоты, собраны в bash скрипт `./installer.sh`.

После чего загрузите исходный код репозитория и установите пакет с зависимостями:

```bash
git clone https://github.com/mitrofanov-m/hh-resume-updater.git 

pip install -r requirements.txt -t ./
```

## Usage
Чтобы начать работу с пакетом - импортируйте его:
```python
import hhbot
# or
from hhbot.driver import HeadHunterBot
```
Примеры использования данного пакета можно найти в `/scripts`.
```python
def push_higher_in_search():
    # используем констукцию with для безопасного открытия контекстного менеджера
    with HeadHunterBot(EMAIL, HH_PASSWORD, HH_RESUME,
            email_settings, invisible=False) as bot:
        bot.start()
        print("logined quite")
        bot.update_resume()
        sleep(10)
```
После того, как вы удостоверитесь, что скрипт рабоает исправно, измените параметр `invisible` на `True`. Теперь вы можете настроить автоматизацию процесса с помощью linux утилиты `cron`.

## Requirements
```
beautifulsoup4==4.9.3
selenium==3.141.0
```
## License
- Данный репозиторий предназначен исключительно для образовательных целей по освоению навыков python (PEP8, ООП, пакетирование), web-scraping и git. 
- Разработчик не рекомендует использование данного пакета на hh.ru, поскольку это может противоречить правилам пользования сайтом и привести к удалению аккаунта.