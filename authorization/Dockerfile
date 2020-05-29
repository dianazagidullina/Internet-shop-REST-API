FROM python:3.7

WORKDIR /server/

ADD requirements.txt /app/
RUN apt-get update \
    && apt-get clean \
    && apt-get update -qqq \
    && pip install --upgrade pip \ 
    && pip install -r /app/requirements.txt

ADD *.py /server/


