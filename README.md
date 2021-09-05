# HeadHunter resume updater
Когда задачу можно решить за 10 минут, но ты нашёл способ автоматизировать решение за 10 дней:
<p align="center">
  <img src="./mem.jpg"  alt="drawing" width="80%"/>
</p>


Сервис hh.ru предоставляет следующую систему заинтересованности соискателя:
```
"Как сделать так, чтобы ваше резюме оказалось ближе к топу выдачи, а не к концу? 
<...> чаще обновляйте ваше резюме — поисковая выдача у работодателей выстраивается в том числе по дате обновления, а значит, после обновления даты ваше резюме поднимается выше. <...> " 
```
Ручное обновление резюме - рутинная задача, а стоимость встроенного функционала автообновления достаточно высока. Данный репозиторий демонстрирует пример создания python библиотеки для автоматизации процесса обновления резюме.


## Installation
**// переписать на короткую инсталляцию и в конце предложить скрипт**

Все описанные ниже команды для простоты собраны в bash скрипт `./installer`.

В случае, если у вас отсутствует браузер chrome - установите его. Ниже приведены команды для установки браузера через терминал:
```bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

sudo apt install ./google-chrome*.deb

sudo apt-get install -f
```
Затем, установите соответствующий драйвер. Он потребуется для взаимодействия selenium с браузером:
```bash
# Install ChromeDriver.
CHROME_DRIVER_VERSION=`curl -sS https://chromedriver.storage.googleapis.com/LATEST_RELEASE`

wget -N https://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip -P ~/

unzip ~/chromedriver_linux64.zip -d ~/

rm ~/chromedriver_linux64.zip

sudo mv -f ~/chromedriver /usr/local/bin/chromedriver

sudo chown root:root /usr/local/bin/chromedriver

sudo chmod 0755 /usr/local/bin/chromedriver

```

После чего загрузите исходный код репозитория и установите зависимости:

```bash
git clone https://github.com/mitrofanov-m/hh-resume-updater.git 

pip install -r requirements.txt -t ./

```

## Usage
Примеры использования данного пакета можно найти в `/scripts`.
```python
def push_higher_in_search():
    # используем констукцию with для безопасного открытия контекстного менеджера
    with HeadHunterBot(EMAIL, HH_PASSWORD, HH_RESUME, email_settings, invisible=False) as bot:
        bot.start()
        print("logined quite")
        bot.update_resume()
        sleep(10)
```
## Requirements

## License
- mit
- разработчик данного пакета не рекомендует к установке на основной аккаунт hh.ru
