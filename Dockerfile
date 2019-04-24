FROM python:3.6.5-slim-stretch
ENV PYTHONBUFFERED 1
RUN apt-get update && apt-get install -y gcc libpq-dev
RUN mkdir /code
WORKDIR /code
ADD pip-requirements /code/
RUN pip install --upgrade pip && pip install -r pip-requirements
ADD . /code/
RUN apt-get remove -y gcc libpq-dev
