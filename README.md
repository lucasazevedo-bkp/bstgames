# BST Games
> Buy, Sell and Trade used games.

![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Python Version](https://img.shields.io/badge/python-3.8.12-blue)
![PostgreSQL Version](https://img.shields.io/badge/postgres-13.5-blue)
![Django Version](https://img.shields.io/badge/django-3.2.6-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Installation

**With Docker**:

Add an .env file in the root directory with the following variables:

```sh  
# .env content
# for example, COMPOSE_PROJECT_NAME=bstgames
COMPOSE_PROJECT_NAME=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_HOST=db # it must be "db" if you are using Docker
DJANGO_SECRET_KEY=
```

And then, run the following command in the root directory:

```sh  
docker-compose up
```

**Without Docker** (Remember that Python and PostgreSQL are needed, i recommend using a virtualenv): 

Set the above environment variables on your OS and then run the following commands in the root directory:

```sh
pip install -r requirements.txt
python manage.py runserver
```

Create superuser to access /admin, run the following command in the root directory:

```sh
# With Docker
docker exec -it bstgames_web python manage.py createsuperuser

# Without Docker
python manage.py createsuperuser
```