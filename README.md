# [vmk-notifier-bot](https://t.me/ivmiit_notifier_bot)
### Бот, который показывает место в списке поступающих ИВМИиТ КФУ и может уведомлять тебя с определенной периодичностью.

## Как запустить?:
1. Скачать и запустить [Docker](https://www.docker.com)
2. Скачать репозиторий. `git clone https://github.com/pavelkochkin1/vmk-notifier-bot.git`
3. Создать образ `docker-compose build`
4. Запустить докер контейнер `docker run -d [IMAGE ID]`
5. Старт контейнера `docker start [CONTAINER ID]`

## Source code
* [data](data/) содержит конфиг бота
* [utils](utils/) содержит класс парсера, класс базыданных и 
* [loader.py](loader.py) подгружает нужные классы и самого бота
* [app.py] включает в себя всю
* [Dockerfile](Dockerfile) логика сервера для загрузки бота


