# Проектная работа 6 спринта

Командная работа https://github.com/AnnaKPolyakova/Auth_sprint_1


Создает индексы person, genre и заполняет данными из бд postgres
(запуск через db_updater.py в отдельном контейнере)
Апи для получения данных из es о фильмах, персонах, жанрах  

Технологии и требования:
```
Python 3.9+
Flask
``` 

### Настройки Docker

##### Установка

* [Подробное руководство по установке](https://docs.docker.com/install/linux/docker-ce/ubuntu/)

### Настройки Docker-compose

##### Установка

* [Подробное руководство по установке](https://docs.docker.com/compose/install/)

### Запуск приложения

#### Перед запуском проекта создаем переменные окружения
Создаем в корне .env и добавляем в него необходимые переменные  
Пример в .env.example - для запуска приложения/тестов целиком в docker  
Пример в .env.example-local - для запуска приложения/тестов локально и 
частично в docker

#### Admin user
После запуска приложения автоматический создается user c is_superuser = True  

* `login: admin`  
* `password: admin` 


#### Запуск проекта полностью в контейнерах docker

* `docker-compose up --build`

Для остановки контейнера:  
* `docker-compose down --rmi all --volumes`

#### Запуск проекта частично в контейнерах docker (redis и elastic)

* `docker-compose -f docker-compose-local.yml up --build`
* `python -m flask_app.pywsgi`

Документация по адресу:  
http://127.0.0.1:5000/v1/doc/redoc/ or или  
http://127.0.0.1:5000/v1/doc/swagger/  

Для остановки контейнера:  
* `docker-compose -f docker-compose-local.yml down --rmi all --volumes`


### Тестирование  

Создаем в папке tests/functional файл с названием .env_test и добавляем в него 
необходимые переменные  
Пример в .env_test.example - для запуска тестов целиком в docker  
Пример в .env_test.example - local - для запуска тестов локально и 
частично в docker


#### Запуск тестов в контейнере docker  

* `docker-compose -f tests/functional/docker-compose-test.yml up --build`

Для остановки контейнера: 
* `docker-compose -f tests/functional/docker-compose-test.yml down --rmi all`

#### Запуск тестов частично в контейнере docker  

* `docker-compose -f tests/functional/docker-compose-test-local.yml up --build`
* `pytest tests/functional/src`

Для остановки контейнера: 
* `docker-compose -f tests/functional/docker-compose-test-local.yml down --rmi all`