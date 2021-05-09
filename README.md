# HeadHunter resume updater

## Note: 
- run weekly time updater with cron on Sunday.
- run schedule runner with cron on Sunday.
- run bot with schedule runner from Monday to Saturday.

## TODO list:
- ~~stable context manager(override init/enter methods)~~ 
- ~~parsing email code~~
- ~~saving cookies~~
- ~~invisible mode~~
- fake user-agent ([click][1], [clack][2])
- swithing like a mobile ([click][4], [clack][5], [click][6], [clack][7])
    - user-agent switcher
- best time searcher
    - ~~parse times~~
    - ~~split by N clusters (best time to update)~~

- good logging system
- run in docker ([click][3])
- not constant timeout
- password login
    - добавить движение мыши для обхода капчи

Selenium docs: https://selenium-python.readthedocs.io/api.html


[1]: https://stackoverflow.com/questions/49565042/way-to-change-google-chrome-user-agent-in-selenium
[2]: https://stackoverflow.com/questions/29916054/change-user-agent-for-selenium-web-driver
[3]: https://stackoverflow.com/questions/57463616/disable-dev-shm-usage-does-not-resolve-the-chrome-crash-issue-in-docker
[4]: https://chromedriver.chromium.org/mobile-emulation
[5]: https://bitbar.com/blog/how-to-use-selenium-for-cross-browser-testing-on-mobile-devices/
[6]: https://gist.github.com/devinmancuso/ec8ae08fa73402e45bf1
[7]:https://sites.google.com/a/chromium.org/chromedriver/mobile-emulation

