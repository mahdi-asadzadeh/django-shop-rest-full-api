FROM python:3.9
LABEL MAINTAINER="Mahdi Asadzadeh | https://mahdiasadzadeh.com | mahdi.asadzadeh.programing@gmail.com"

ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app
COPY . /app

COPY requirements.txt /app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt


CMD ["gunicorn", "--chdir", "config", "--bind", ":8000", "config.wsgi:application"]