
FROM python:3.8

WORKDIR /app
COPY ./requirements.txt ./app/

RUN pip install --no-cache-dir --upgrade -r ./app/requirements.txt

COPY . ./app

CMD ["uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8080"]
