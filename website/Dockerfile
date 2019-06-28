FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /website
WORKDIR /website
COPY requirements.txt /website
RUN pip install -r requirements.txt
COPY . /website