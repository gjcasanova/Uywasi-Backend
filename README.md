# Uywasi Backend 
![Uywasi logo](https://scontent.fuio17-1.fna.fbcdn.net/v/t1.15752-9/120455162_1054269088378451_4640175083028828593_n.png?_nc_cat=104&_nc_sid=ae9488&_nc_ohc=IS4HblxVbQEAX-PvF1-&_nc_ht=scontent.fuio17-1.fna&oh=1d38728b3288d8e9c37a2c0bc864e2b2&oe=5F9A404B)

Uywasi is a web app for lookup lost pets. This repository contains the backend project. This file is based on development environment.

## 1. Requirements

 - docker 19.03.13 or higher.
 - docker-compose 1.27.4 or higher.

## 2. Third party tools and services
 
### 2.1. Services running on docker
 
 - [django](https://github.com/django/django)
 - [postgres](https://github.com/postgres/postgres)
 - [docs](https://github.com/sphinx-doc/sphinx) 
 - [mailhog](https://github.com/mailhog/MailHog)
 - [redis](https://github.com/redis/redis)
 - [celeryworker](https://github.com/celery/celery)
 - [celerybeat](https://github.com/celery/celery)
 - [flower](https://github.com/mher/flower)

### 2.2. Tools
 
 - [cookiecutter-django](https://github.com/pydanny/cookiecutter-django)

## 3. How to run this project

### 3.0. Clone this repository

    $ git clone https://github.com/GuillermoMCasanova/Uywasi-Backend.git

### 3.1. Building docker images

    $ sudo docker-compose -f local.yml build

### 3.2. Running docker containers
 
    $ sudo docker-compose -f local.yml up

### 3.3. Checking docker status
 
    $ sudo docker-compose -f local.yml ps

### 3.4. Stopping docker containers
 
    $ sudo docker-compose -f local.yml down

### 3.5. Running commands on docker containers
 
    $ sudo docker-compose -f local.yml build

### 3.6. For debugging

For create a break points for debug the code:

    import ipdb; ipdb.set_trace()

Then is necessary run the django container in other console individually:

    $ sudo docker-compose -f local.yml run --rm --service-ports django

### 3.7. For execute commands into containers
For execute commands into containers is necessary follow this format:

    $ sudo docker-compose -f local.yml run --rm <image_name> <command>
    
For example:

    $ sudo docker-compose -f local.yml run --rm django python manage.py migrate

 
## 4. Sites for visit
 
 - [Web API ](http://localhost:8000/) http://localhost:8000/
 - [Docs](http://localhost:7000/) http://localhost:7000/
 - [Mailhog](http://localhost:8025/) http://localhost:8025/
 - [Flower](http://localhost:5555/) http://localhost:5555/

## 5. More info
For more info go to the official docs of the tools:

 - [docker](https://docs.docker.com/)
 - [docker-compose](https://docs.docker.com/compose/)
 - [cookiecutter-django](https://cookiecutter-django.readthedocs.io/en/latest/)
 - [django](https://docs.djangoproject.com/en/3.1/)
