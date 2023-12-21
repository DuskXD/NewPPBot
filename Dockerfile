FROM python:3.11

WORKDIR /NewPPBot

COPY requirements.txt /NewPPBot
RUN pip install --upgrade pip -r requirements.txt

COPY . /NewPPBot

EXPOSE 5000


