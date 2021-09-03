# HeadHunter resume updater
Когда задачу можно решить за 10 минут, но ты нашёл способ автоматизировать решение за 10 дней:

![Alt text](./mem.jpg?raw=true "mem")

Сервис hh.ru предоставляет следующую систему заинтересованности соискателя:
```
"Как сделать так, чтобы ваше резюме оказалось ближе к топу выдачи, а не к концу? 
<...> чаще обновляйте ваше резюме — поисковая выдача у работодателей выстраивается в том числе по дате обновления, а значит, после обновления даты ваше резюме поднимается выше. <...> " 
```
Ручное обновление резюме - рутинная задача, а стоимость встроенного функционала автообновления достаточно высока. Данный репозиторий демонстрирует пример создания python библиотеки для автоматизации процесса обновления резюме.


## Installation

В случае, если у вас отсутствует браузер chrome - установите его. Ниже приведены команды для установки браузера через терминал:
```
CHROME_DRIVER_VERSION=`curl -sS https://chromedriver.storage.googleapis.com/LATEST_RELEASE`

wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

sudo apt install ./google-chrome*.deb

sudo apt-get install -f
```
Затем, установите соответствующий драйвер. Он потребуется для взаимодействия selenium с браузером:
```
# Install ChromeDriver.
wget -N https://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip -P ~/

unzip ~/chromedriver_linux64.zip -d ~/

rm ~/chromedriver_linux64.zip

sudo mv -f ~/chromedriver /usr/local/bin/chromedriver

sudo chown root:root /usr/local/bin/chromedriver

sudo chmod 0755 /usr/local/bin/chromedriver

```

После чего загрузите исходный код репозитория и установите зависимости:

```
git clone https://github.com/mitrofanov-m/hh-resume-updater.git 

python -m pip install -r requirements.txt
```



## Usage

## Requirements

## License
- mit
- разработчик данного пакета не рекомендует к установке на основной аккаунт hh.ru

