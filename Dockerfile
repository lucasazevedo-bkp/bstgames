FROM python:3.8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get install -y \
    gettext postgresql-client \
    && pip install -r requirements.txt
COPY . .