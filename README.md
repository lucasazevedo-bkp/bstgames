# BST Games
> Buy, Sell and Trade used games.

![Ubuntu Version](https://img.shields.io/badge/ubuntu-20.04-blue)
![Docker](https://img.shields.io/badge/docker-wsl2-blue)
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
# if you are using Docker, it must be "db" for POSTGRES_HOST=db
POSTGRES_HOST= 
DJANGO_SECRET_KEY=
```

Run the following command in the root directory:

```sh  
docker-compose up
```

**Without Docker**: 

Remember that Python and PostgreSQL (create the database manually) are needed, i recommend using a virtualenv. 
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