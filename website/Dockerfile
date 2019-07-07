FROM python:3

ENV PYTHONUNBUFFERED 1
RUN mkdir /website
COPY . /website
WORKDIR /website
RUN pip install -r requirements.txt