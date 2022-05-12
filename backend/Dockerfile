
FROM python:3.9

WORKDIR /

COPY ./Pipfile /code/Pipfile
COPY ./Pipfile.lock /code/Pipfile.lock

RUN pipenv install

#
COPY . /app

#
CMD ["pipenv", "startdev"]
