FROM python:3.7
#WORKDIR /server/

ADD server/requirements.txt /app/
RUN apt-get update \
    && apt-get clean \
    && apt-get update -qqq \
    && pip install --upgrade pip \ 
    && pip install -r /app/requirements.txt

ADD server/*.py /server/

ADD authorization/authconfig.py /server/
