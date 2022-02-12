# BST Games
> Buy, Sell and Trade used games.

![Ubuntu Version](https://img.shields.io/badge/ubuntu-20.04-blue)
![Docker](https://img.shields.io/badge/docker-wsl2-blue)
![Python Version](https://img.shields.io/badge/python-3.8.12-blue)
![PostgreSQL Version](https://img.shields.io/badge/postgres-13.5-blue)
![Django Version](https://img.shields.io/badge/django-3.2.6-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Installation

Go to the root directory:

**With Docker**:

Add "web.env" and "db.env" files and fill in the variables:

```sh  
# web.env
COMPOSE_PROJECT_NAME=
DJANGO_SECRET_KEY=

# db.env 
POSTGRES_USER=
POSTGRES_PASSWORD=
```

Run: docker, migrations, fixtures and create superuser to access /admin:

```sh  
docker-compose up
# Open new terminal
docker exec bstgames_web python manage.py migrate
# Run fixtures only if you want to populate the database
docker exec bstgames_web python manage.py loaddata bstgames.json
docker exec -it bstgames_web python manage.py createsuperuser
```

**Without Docker**:
 
Add "web.env" and "db.env" files and fill in the variables:

```sh  
# web.env
DJANGO_SECRET_KEY=

# db.env 
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_HOST=
```

Install the requirements, run: migrations, fixtures, server and create superuser to access /admin:

```sh
pip install -r requirements.txt
python manage.py migrate
# Run fixtures only if you want to populate the database
python manage.py loaddata bstgames.json
python manage.py createsuperuser
python manage.py runserver
```