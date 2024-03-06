FROM python:3.12-alpine

WORKDIR /backend

COPY ./requirements.txt /backend

RUN pip install -r requirements.txt

COPY . /backend



CMD [ "gunicorn","--bind","0.0.0.0:8000","backend.wsgi" ]