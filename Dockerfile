FROM ubuntu:latest
# ubuntu:latest
# python3.8-slim-buster

ENV PYTHONUNBUFFERED = 1
WORKDIR /django

RUN apt-get update && apt-get install -y \
    python3-pip

COPY requirements.txt requirements.txt
# # RUN apt install python3-pip
RUN pip3 install -r requirements.txt

# COPY . .

# CMD ["python3","manage.py","runserver","0.0.0.0:8000"]