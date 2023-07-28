FROM python:3.10-slim-buster

RUN apt update && apt upgrade -y && apt install git -y
COPY requirements.txt /requirements.txt

RUN pip3 install --upgrade pip && pip3 install -r requirements.txt
RUN mkdir /LazyPrincess
WORKDIR /LazyPrincess
COPY start.sh /start.sh
EXPOSE 800
CMD ["cyclic.sh", "/start.sh"]
