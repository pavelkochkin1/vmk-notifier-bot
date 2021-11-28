# [vmk-notifier-bot](https://t.me/ivmiit_notifier_bot)
### Бот, который показывает место в списке поступающих ИВМИиТ КФУ и может уведомлять тебя с определенной периодичностью.

## Как запустить?:
1. Скачать и запустить [Docker](https://www.docker.com)
2. Скачать репозиторий. `git clone https://github.com/pavelkochkin1/vmk-notifier-bot.git`
3. Создать образ `docker-compose build`
4. Запустить докер контейнер `docker run -d [IMAGE ID]`
5. Старт контейнера `docker start [CONTAINER ID]`

## Source code
* [simpsons_baseline.ipynb](simpsons_baseline.ipynb) contains my research
* [demo.py](demo.py) contains server logic
* [model/model.py](model/model.py) class of model
* [templates](templates/) and [static](static/) includes html and css files for app
* [Dockerfile](Dockerfile) describes a Docker image that is used to run the app

## Example
1. Run the docker container and open the `http://localhost:8888/`.
![alt text](ref/first.png)
2. Upload your image and press `Predict` button.
![alt text](ref/second.png)
3. Now we have prediction and probability.
![alt text](ref/third.png)

