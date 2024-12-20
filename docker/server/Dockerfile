FROM python:3.10

WORKDIR /server

COPY ./docker/server/requirements.txt /server/requirements.txt

RUN pip install --upgrade pip && pip install --no-cache-dir --upgrade -r /server/requirements.txt

COPY /server /server
COPY /.env /server/.env

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
